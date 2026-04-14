import requests
import random
from jsonschema import validate

import schemas.club_schema
from tests.auth.conftest import USERNAME, PASSWORD, API_URL


def test_success_create_club(access_token, valid_club_body):
    """Тест: Успешное создание клуба."""
    headers = {"Authorization": f"Bearer {access_token}"}

    club_response = requests.post(API_URL + "/clubs/", headers=headers, json=valid_club_body)

    print(f"\nStatus code: {club_response.status_code}\nBody: {club_response.text}")

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    # Валидация схемы остается здесь, так как она специфична для этого теста
    validate(instance=club_response_body, schema=schemas.club_schema.success_create_club)


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

    print(
        f"--- Создание клуба без авторизации ---\n"
        f"\nStatus: {club_response.status_code}\n"
        f"Headers: {club_response.headers}\n"
        f"Body: {club_response.text}"
    )
    assert club_response.status_code == 401, f"Ожидался статус 401, получен {club_response.status_code}"

    # 2. Проверка текста ошибки
    body = club_response.json()
    assert body.get("detail") in [
        "Authentication credentials were not provided.",
        "Учетные данные не были предоставлены."
    ], f"Неожиданное сообщение об ошибке: {body.get('detail')}"


def test_create_club_with_invalid_data(access_token):
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

    print(
        f"--- Создание клуба с некорректными данными ---\n"
        f"\nStatus: {club_response.status_code}\n"
        f"Headers: {club_response.headers}\n"
        f"Body: {club_response.text}"
    )
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

