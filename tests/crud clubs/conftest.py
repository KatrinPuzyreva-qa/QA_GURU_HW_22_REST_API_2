import pytest
import requests
import random
from tests.auth.conftest import USERNAME, PASSWORD, API_URL

# Фикстура для получения access_token
@pytest.fixture(scope="session")
def access_token():
    """Получает access token для авторизованных тестов."""
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    assert auth_response.status_code == 200, "Не удалось получить токен авторизации"
    return auth_response.json()["access"]

# Фикстура для валидных данных клуба
@pytest.fixture
def valid_club_body():
    """Возвращает словарь с валидными данными для создания клуба."""
    return {
        "bookTitle": f"Test Book {random.randint(1000, 999999)}",
        "bookAuthors": "Test Author",
        "publicationYear": 2024,
        "description": "Valid description",
        "telegramChatLink": "https://t.me/valid_link"
    }