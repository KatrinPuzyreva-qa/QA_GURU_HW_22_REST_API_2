import requests
import random
from jsonschema import validate
from Schemas.club_schema import success_create_club

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "katrin"
PASSWORD = "katrin1"
TOKEN_PATH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
USERNAME_ID = 1772

def test_success_create_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    book_title = f"Some another book {random.randint(1000, 999999)}"
    book_author = f"Some author"
    club_body = {
      "bookTitle": book_title,
      "bookAuthors": book_author,
      "publicationYear": 2147483647,
      "description": "Some descr",
      "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    validate(club_response_body, schema=success_create_club)

    assert club_response_body["bookTitle"] == book_title
    assert club_response_body["bookAuthors"] == book_author
    # todo other fields
    assert club_response_body["owner"] == USERNAME_ID
    assert USERNAME_ID in club_response_body["members"]
    assert len(club_response_body["reviews"]) == 0
    assert club_response_body["modified"] is None

    club_id = club_response_body["id"]
    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204


def test_create_club_unauthorized():
    """Тест: Попытка создать клуб без токена авторизации."""

    book_title = f"Unauthorized Book {random.randint(1000, 999999)}"
    club_body = {
        "bookTitle": book_title,
        "bookAuthors": "Some author",
        "publicationYear": 2147483647,
        "description": "Should fail",
        "telegramChatLink": "https://t.me/qa.guru"
    }

    # Запрос отправляется БЕЗ заголовка Authorization
    club_response = requests.post(API_URL + "/clubs/", json=club_body)

    print("\n--- Создание клуба без авторизации ---")
    print("Status code:", club_response.status_code)
    print("Body:", club_response.text)

    assert club_response.status_code == 401, f"Ожидался статус 401, получен {club_response.status_code}"

    # 2. Проверка текста ошибки
    body = club_response.json()
    assert body.get("detail") in [
        "Authentication credentials were not provided.",
        "Учетные данные не были предоставлены."
    ], f"Неожиданное сообщение об ошибке: {body.get('detail')}"


def test_create_club_with_invalid_data():
    """Тест: Создание клуба с некорректными данными в payload."""
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]
    headers = {"Authorization": f"Bearer {access_token}"}

    invalid_club_body = {
        "bookTitle": "",  # Нарушение: пустое обязательное поле
        "bookAuthors": "Test Author",
        "publicationYear": 2025,  # Валидный год, так как сервер не проверяет диапазон
        "description": "Invalid data test",
        "telegramChatLink": "t.me/invalid_link"  # Нарушение: некорректный формат URL
    }

    club_response = requests.post(API_URL + "/clubs/", headers=headers, json=invalid_club_body)

    print("\\n--- Создание клуба с некорректными данными ---")
    print("Status code:", club_response.status_code)
    print("Body:", club_response.text)

    # Проверка статуса ответа
    assert club_response.status_code == 400, f"Ожидался статус 400, получен {club_response.status_code}"

    # Проверка структуры ответа с ошибками валидации
    body = club_response.json()

    # Проверяем ошибки для полей, которые ДЕЙСТВИТЕЛЬНО проверил сервер
    assert "bookTitle" in body and "This field may not be blank." in body["bookTitle"]
    assert "telegramChatLink" in body and "Enter a valid URL." in body["telegramChatLink"]

    # Проверка того, что сервер НЕ вернул ошибку для publicationYear,
    # так как он его не валидирует.
    assert "publicationYear" not in body, \
        "Сервер не должен был проверять поле publicationYear, но вернул ошибку."