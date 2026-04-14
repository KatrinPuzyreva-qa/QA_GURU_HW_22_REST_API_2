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

# 3. Фикстура для заголовков (зависит от access_token)
@pytest.fixture
def auth_headers(access_token):
    """Фикстура, возвращающая словарь заголовков с Authorization."""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
@pytest.fixture
def valid_club_id():
    """
    Фикстура, которая получает список клубов и возвращает ID первого найденного.
    Если список пуст, тест, использующий эту фикстуру, будет помечен как xfail.
    """
    list_url = f"{API_URL}/clubs/"
    list_response = requests.get(list_url)

    # Проверяем, что сам эндпоинт списка работает
    assert list_response.status_code == 200, "Не удалось получить доступ к списку клубов"

    list_body = list_response.json()

    # Проверяем наличие данных
    if "results" in list_body and len(list_body["results"]) > 0:
        return list_body["results"][0]["id"]
    else:
        pytest.xfail("Список клубов пуст. Невозможно выполнить тест, требующий валидный ID клуба.")



# 2. Фикстура для создания и очистки клуба (с использованием yield)
@pytest.fixture
def club_for_deletion(auth_headers):
    """
    Фикстура создает клуб и возвращает его ID.
    После завершения теста (даже в случае ошибки) фикстура удаляет созданный клуб.
    """
    # --- Этап Setup (до yield) ---
    book_title = f"Book for Deletion {random.randint(1000, 9999)}"
    club_body = {
        "bookTitle": book_title,
        "bookAuthors": "Test Author",
        "publicationYear": 2024,
        "description": "This club will be deleted",
        "telegramChatLink": "https://t.me/qa.guru"
    }

    create_response = requests.post(f"{API_URL}/clubs/", headers=auth_headers, json=club_body)

    # Проверяем, что создание прошло успешно
    assert create_response.status_code == 201, f"Не удалось создать клуб для теста: {create_response.text}"

    club_id = create_response.json()["id"]
    print(f"➕ Создан клуб с ID {club_id} для теста удаления.")

    # Отдаем ID теста в сам тест
    yield club_id

    # --- Этап Teardown (после yield) ---
    # Этот код выполнится всегда, даже если тест упал.
    delete_response = requests.delete(f"{API_URL}/clubs/{club_id}/", headers=auth_headers)

    # Код 404 здесь нормален, если тест на удаление прошел успешно и удалил клуб.
    # Код 204 — если мы удаляем его здесь.
    # Любая другая ошибка — повод для дебага.
    if delete_response.status_code not in [204, 404]:
        print(f"⚠️  Не удалось очистить клуб {club_id} после теста. Статус: {delete_response.status_code}")


# 3. Фикстура для несуществующего ID (константа)
@pytest.fixture
def non_existent_club_id():
    """Возвращает ID клуба, который не существует в системе."""
    return 999999  # Или любая другая логика генерации уникального несуществующего ID