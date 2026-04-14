import requests
from jsonschema import validate
from schemas.club_schema import response_schema_get

BASE_URL = "https://book-club.qa.guru/api/v1"

def test_get_id():
    response = requests.get(f"{BASE_URL}/clubs/886")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()

    assert body['id'] == 886
    print(f"🎉 Test passed: API correctly found books containing")


def test_get_single_club_by_id():
    club_id = 886
    url = f"{BASE_URL}/clubs/{club_id}"

    response = requests.get(url)

    print("\n--- Testing GET Single Club (ID: 886) ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    # Проверяем, что клуб найден
    assert response.status_code == 200, f"Club with ID {club_id} not found"

    body = response.json()

    # Валидация структуры ответа по схеме ОДНОГО клуба
    validate(instance=body, schema=response_schema_get)

    # Дополнительная проверка данных (что это действительно тот клуб)
    assert body['id'] == club_id, "Returned club ID does not match requested ID"
    assert body['bookTitle'] == "booking_info", "Book title does not match expected value for ID 886"

    print("✅ Test passed: Club structure is valid and data matches.")


def test_get_single_club_full_validation():
    """
    Тест: Получение списка клубов -> Выбор первого ID -> Валидация структуры и данных одного клуба.
    Проверяет, что API возвращает корректную структуру и валидные данные.
    """
    # 1. Получаем список клубов, чтобы найти валидный ID
    list_url = f"{BASE_URL}/clubs/"
    list_response = requests.get(list_url)

    print("\n--- ЭТАП 1: Получение списка клубов ---")
    print("Status code (список):", list_response.status_code)
    # print("Body (список):", list_response.text) # Раскомментируйте для отладки

    # Проверяем, что список клубов доступен
    assert list_response.status_code == 200, "Не удалось получить список клубов"

    list_body = list_response.json()

    # Проверяем, что в списке есть хотя бы один клуб
    # (Предполагаем, что API возвращает {"results": [ ... ]})
    assert "results" in list_body and len(list_body["results"]) > 0, "Список клубов пуст"

    # Берем ID первого клуба из списка
    club_id = list_body["results"][0]["id"]
    print(f"Выбран ID клуба для проверки: {club_id}")

    # 2. Получаем данные конкретного клуба по ID
    detail_url = f"{BASE_URL}/clubs/{club_id}/"
    detail_response = requests.get(detail_url)

    print("\n--- ЭТАП 2: Валидация данных клуба ---")
    print("Status code (детали):", detail_response.status_code)
    # print("Body (детали):", detail_response.text) # Раскомментируйте для отладки

    assert detail_response.status_code == 200, f"Не удалось получить клуб с ID {club_id}"

    club_body = detail_response.json()

    # 3. Валидация структуры ответа по JSON Schema
    print("\n--- ЭТАП 3: Валидация по JSON Schema ---")
    validate(instance=club_body, schema=response_schema_get)
    print("✅ Структура данных соответствует схеме.")

    # 4. Дополнительные проверки (смарт-ассерты)
    print("\n--- ЭТАП 4: Проверка значений ---")

    # Проверка соответствия ID
    assert club_body["id"] == club_id, "ID в ответе не совпадает с запрошенным"

    # Проверка на пустые строки (название и автор не должны быть пустыми)
    assert club_body["bookTitle"].strip() != "", "Название книги не должно быть пустым"
    assert club_body["bookAuthors"].strip() != "", "Имя автора не должно быть пустым"

    # Проверка логики: Владелец должен быть в списке членов клуба
    assert club_body["owner"] in club_body["members"], "Владелец не состоит в списке members"

    # Проверка типа и диапазона года публикации (базовая проверка на реальность)
    assert isinstance(club_body["publicationYear"], int), "Год публикации должен быть числом"

    print("✅ Все проверки пройдены. Данные валидны.")