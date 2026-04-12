import requests
import random

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "katrin"
PASSWORD = "katrin1"
USERNAME_ID = 1772


def test_delete_club():
    """
    Тест: Создание клуба -> Удаление клуба -> Проверка, что клуб недоступен.
    """
    # 1. Авторизация
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)

    # Проверяем, что авторизация прошла успешно
    assert auth_response.status_code == 200, f"Авторизация не удалась: {auth_response.text}"

    access_token = auth_response.json()["access"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Создание клуба (Этап Create)
    book_title = f"Book for Deletion {random.randint(1000, 9999)}"
    club_body = {
        "bookTitle": book_title,
        "bookAuthors": "Test Author",
        "publicationYear": 2024,
        "description": "This club will be deleted",
        "telegramChatLink": "https://t.me/qa.guru"
    }

    create_response = requests.post(API_URL + "/clubs/", headers=headers, json=club_body)

    print("\n--- ЭТАП СОЗДАНИЯ ---")
    print("Status code:", create_response.status_code)
    print("Body:", create_response.text)

    # Проверяем, что клуб создан успешно (статус 201 Created)
    assert create_response.status_code == 201, f"Не удалось создать клуб: {create_response.text}"

    club_id = create_response.json()["id"]
    print(f"✅ Клуб успешно создан с ID: {club_id}")

    # 3. Удаление клуба (Этап Delete)
    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=headers)

    print("\n--- ЭТАП УДАЛЕНИЯ ---")
    print("Status code DELETE:", delete_response.status_code)

    # Проверяем, что удаление прошло успешно (статус 204 No Content)
    assert delete_response.status_code == 204, f"Ожидался код 204 при удалении, получен: {delete_response.status_code}"

    print("✅ Клуб успешно удален.")

    # 4. Проверка удаления (Этап Read после Delete)
    get_response = requests.get(API_URL + f"/clubs/{club_id}/", headers=headers)

    print("\n--- ЭТАП ПРОВЕРКИ УДАЛЕНИЯ ---")
    print("Status code GET (после удаления):", get_response.status_code)

    # Проверяем, что клуб действительно не найден (статус 404 Not Found)
    assert get_response.status_code == 404, f"Ожидался код 404 (клуб не найден), но пришел: {get_response.status_code}"

    print("✅ Тест пройден: Клуб успешно удален и больше не доступен при получении списка клубов.")


def test_delete_nonexistent_club():
    """
    Тест: Попытка удалить клуб с несуществующим ID.
    Ожидаемый результат: Статус 404 Not Found.
    """
    # Используем ID, который точно не существует в системе
    NON_EXISTENT_CLUB_ID = 999999

    # Авторизация (используем пользователя с правами)
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    assert auth_response.status_code == 200
    access_token = auth_response.json()["access"]

    headers = {"Authorization": f"Bearer {access_token}"}

    # Попытка удаления
    delete_response = requests.delete(
        f"{API_URL}/clubs/{NON_EXISTENT_CLUB_ID}/",
        headers=headers
    )

    print("\n--- Удаление несуществующего клуба ---")
    print("Status code:", delete_response.status_code)
    print("Body:", delete_response.text)

    # Проверка статуса
    assert delete_response.status_code == 404, f"Ожидался статус 404, получен {delete_response.status_code}"

    # Проверка тела ответа (если API возвращает JSON)
    body = delete_response.json()
    assert "detail" in body
    assert isinstance(body["detail"], str)

    print("✅ Тест пройден: API корректно обработал запрос на удаление несуществующего объекта.")

