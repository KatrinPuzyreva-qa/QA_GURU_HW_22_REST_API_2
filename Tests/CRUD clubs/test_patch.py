import requests
import json

API_URL = "https://book-club.qa.guru/api/v1"
CLUB_ID = 162
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"  # <-- ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ТОКЕН

# Полезная нагрузка (payload) для обновления
PATCH_PAYLOAD = {
    "bookTitle": "booking_info",
    "bookAuthors": "booking_author",
    "publicationYear": 2147483647,
    "description": "description",
    "telegramChatLink": "https://t.me/qa.guru"
}


def test_patch_club_success():
    """Тест: Успешное частичное обновление клуба."""

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
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

    # 1. Проверка статуса ответа
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    # 2. Проверка, что данные в ответе соответствуют отправленным
    body = response.json()

    # Проверяем каждое поле из payload
    assert body["bookTitle"] == PATCH_PAYLOAD["bookTitle"]
    assert body["bookAuthors"] == PATCH_PAYLOAD["bookAuthors"]
    assert body["publicationYear"] == PATCH_PAYLOAD["publicationYear"]
    assert body["description"] == PATCH_PAYLOAD["description"]
    assert body["telegramChatLink"] == PATCH_PAYLOAD["telegramChatLink"]

    # Проверяем, что ID клуба не изменился
    assert body["id"] == CLUB_ID, "ID клуба был изменен при обновлении"


def test_patch_club_empty_body():
    """Тест: Отправка PATCH-запроса с пустым телом."""

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.patch(
        f"{API_URL}/clubs/{CLUB_ID}/",
        headers=headers,
        json={}  # Пустое тело запроса
    )

    print("\\n--- PATCH Пустое тело запроса ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    # 1. Проверка статуса ответа (Ожидается ошибка клиента)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    # 2. Проверка текста ошибки (зависит от реализации бэкенда)
    body = response.json()

    # Обычно бэкенд (например, DRF) возвращает список ошибок для каждого поля
    # или общее сообщение. Проверим типичные варианты.
    assert "non_field_errors" in body or any("required" in err for err in body.values()), \ \
            f"Неожиданная структура ошибки: {body}"