import requests
from jsonschema import validate
from schemas.club_schema import response_schema_get
from tests.auth.conftest import API_URL


def test_get_id():
    response = requests.get(f"{API_URL}/clubs/886")

    print(
        f"--- Получение списка клубов ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Headers: {response.headers}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 200
    body = response.json()

    assert body['id'] == 886


def test_get_single_club_by_dynamic_id(valid_club_id):
    url = f"{API_URL}/clubs/{valid_club_id}/"
    response = requests.get(url)

    print(
        f"--- Получение клуба по ID с полной валидацией ---\n"
        f"Status: {response.status_code}\n"
        f"Body: {response.text}\n"
    )

    # 1. Проверка статуса
    assert response.status_code == 200, f"Club with ID {valid_club_id} not found"

    club_body = response.json()

    # 2. Валидация структуры ответа по JSON Schema
    print("--- Валидация по JSON Schema ---")
    validate(instance=club_body, schema=response_schema_get)

    # 3. Смарт-ассерты (проверка логики и значений)
    print("--- Проверка значений и логики ---")

    # Проверка соответствия ID (защита от ошибки в API)
    assert club_body["id"] == valid_club_id, "ID в ответе не совпадает с запрошенным"

    # Проверка на пустые строки
    assert club_body["bookTitle"].strip() != "", "Название книги не должно быть пустым"
    assert club_body["bookAuthors"].strip() != "", "Имя автора не должно быть пустым"

    # Проверка логики: Владелец должен быть в списке членов клуба
    assert club_body["owner"] in club_body["members"], "Владелец не состоит в списке members"

    # Проверка типа года публикации
    assert isinstance(club_body["publicationYear"], int), "Год публикации должен быть целым числом"
