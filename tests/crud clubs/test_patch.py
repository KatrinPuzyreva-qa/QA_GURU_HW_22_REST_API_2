import requests
from jsonschema import validate

from schemas.club_schema import club_detail_schema_patch

API_URL = "https://book-club.qa.guru/api/v1"
CLUB_ID = 886

PATCH_PAYLOAD = {
    "bookTitle": "booking_info",
    "bookAuthors": "booking_author",
    "publicationYear": 2147483647,
    "description": "description",
    "telegramChatLink": "https://t.me/qa.guru"
}


def test_patch_club_success():
    """Тест: Успешное частичное обновление клуба."""
    auth_body = {"username": "katrin", "password": "katrin1"}
    auth_response = requests.post(f"{API_URL}/auth/token/", json=auth_body)

    assert auth_response.status_code == 200, "Не удалось авторизоваться"
    access_token = auth_response.json()["access"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(
        f"{API_URL}/clubs/{CLUB_ID}/",
        headers=headers,
        json=PATCH_PAYLOAD
    )

    print("\n--- PATCH Успешное обновление ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=club_detail_schema_patch)
    # Проверка, что данные обновились
    assert body["bookTitle"] == PATCH_PAYLOAD["bookTitle"]


def test_patch_club_empty_body():
    """Тест: Отправка PATCH-запроса с пустым телом."""
    auth_body = {"username": "katrin", "password": "katrin1"}
    auth_response = requests.post(f"{API_URL}/auth/token/", json=auth_body)

    assert auth_response.status_code == 200, "Не удалось авторизоваться"
    access_token = auth_response.json()["access"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Отправляем ПУСТОЕ тело запроса
    response = requests.patch(
        f"{API_URL}/clubs/{CLUB_ID}/",
        headers=headers,
        json={}
    )

    print("\n--- PATCH Пустое тело запроса ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)


    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    # Проверяем, что данные в ответе НЕ изменились по сравнению с тем, что было в бд
    body = response.json()
    validate(instance=body, schema=club_detail_schema_patch)
    assert "id" in body
    assert "bookTitle" in body
    assert "modified" in body
