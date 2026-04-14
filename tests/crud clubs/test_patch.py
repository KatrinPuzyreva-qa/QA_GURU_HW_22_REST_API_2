import requests
from jsonschema import validate

from schemas.club_schema import club_detail_schema_patch
from tests.auth.conftest import API_URL, CLUB_ID, PATCH_PAYLOAD


def test_patch_club_success(auth_headers):
    """
    Тест: Успешное частичное обновление клуба.
    Логика авторизации и подготовки данных вынесена в фикстуры.
    """
    url = f"{API_URL}/clubs/{CLUB_ID}/"

    # Используем готовые заголовки и payload
    response = requests.patch(url, headers=auth_headers, json=PATCH_PAYLOAD)

    print(f"--- PATCH Успешное обновление ---\nStatus code: {response.status_code}\nBody: {response.text}\n")

    # Проверка статуса
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=club_detail_schema_patch)

    # Ключевая проверка: данные действительно обновились
    assert body["bookTitle"] == PATCH_PAYLOAD["bookTitle"]


def test_patch_club_empty_body(auth_headers):
    """    Тест: Отправка PATCH-запроса с пустым телом.    """
    url = f"{API_URL}/clubs/{CLUB_ID}/"

    # Используем готовые заголовки, но отправляем пустое тело {}
    response = requests.patch(url, headers=auth_headers, json={})

    print(f"--- PATCH Пустое тело запроса ---\nStatus code: {response.status_code}\nBody: {response.text}\n")

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=club_detail_schema_patch)

    # Проверка наличия ключевых полей в ответе
    assert "id" in body and body["id"] == CLUB_ID
    assert "bookTitle" in body and body["bookTitle"] == PATCH_PAYLOAD["bookTitle"]  # Данные не изменились!
    assert "modified" in body
