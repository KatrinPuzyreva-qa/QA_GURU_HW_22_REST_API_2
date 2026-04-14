import requests
from jsonschema import validate
from schemas.registration_schema import payload_schema, error_username_already_exists_schema, \
    error_password_validation_schema, error_password_required_schema, error_username_validation_schema, \
    error_username_required
from tests.auth.conftest import API_URL


def test_register_user_success(registration_data):
    """Тест успешной регистрации."""
    url = f"{API_URL}/users/register/"
    response = requests.post(url, json=registration_data)

    print(
        f"--- УСПЕШНАЯ Регистрация ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Headers: {response.headers}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=payload_schema)
    assert "id" in body, "В ответе отсутствует поле 'id'"


def test_register_user_existing_username(existing_user_data):
    """Тест регистрации с уже существующим username."""
    url = f"{API_URL}/users/register/"
    response = requests.post(url, json=existing_user_data)

    print(
        f"--- Регистрация существующего пользователя ---\n"
        f"Status: {response.status_code}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 400  # Conflict
    body = response.json()
    validate(instance=body, schema=error_username_already_exists_schema)
    assert "username" in body and isinstance(body["username"], list), "Ответ не содержит массив ошибок для username"

    # Проверяем, что нужное сообщение есть в списке ошибок
    expected_error = "A user with that username already exists."
    assert expected_error in body["username"], f"Ожидалась ошибка '{expected_error}', получена {body['username']}"


def test_register_user_invalid_password(invalid_password_data):
    """Тест регистрации с пустым паролем."""
    url = f"{API_URL}/users/register/"
    response = requests.post(url=url, json=invalid_password_data)

    print(
        f"--- Регистрация с невалидным паролем ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_password_validation_schema)

    assert "password" in body and isinstance(body["password"], list), \
        "Ответ должен содержать ключ 'password' со списком ошибок"

    expected_error = "This field may not be blank."
    assert expected_error in body["password"], \
        f"Ожидалась ошибка '{expected_error}', получен список ошибок: {body['password']}"


def test_register_user_missing_fields(missing_field_data):
    """Тест регистрации с отсутствующим параметром пароля."""
    url = f"{API_URL}/users/register/"
    response = requests.post(url, json=missing_field_data)

    print(
        f"--- Регистрация с с отсутствующим параметром пароля ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 400, f"Ожидался статус 400 (Bad Request), получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_password_required_schema)
    assert "password" in body and isinstance(body["password"], list), \
        f"Ответ должен содержать ключ 'password' со списком ошибок. Получено: {body}"

    expected_error = "This field is required."
    assert expected_error in body["password"], \
        f"Ожидалась ошибка '{expected_error}', получен список ошибок: {body['password']}"


def test_register_user_empty_username(empty_username_data):
    """Тест регистрации с пустым полем username."""
    url = f"{API_URL}/users/register/"
    response = requests.post(url, json=empty_username_data)

    print(
        f"--- Регистрация с пустым username ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_username_validation_schema)

    assert "username" in body, f"Ключ 'username' отсутствует в ответе. Получено: {body}"

    expected_error = "This field may not be blank."
    assert expected_error in body["username"], \
        f"Ожидалась ошибка про пустое поле, получена: {body['username']}"


def test_register_user_missing_username(missing_username_data):
    """Тест регистрации с отсутствующим параметром username."""

    url = f"{API_URL}/users/register/"
    response = requests.post(url, json=missing_username_data)

    print(
        f"--- Регистрация с отсутствующим username ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_username_required)

    assert "username" in body, f"Ключ 'username' отсутствует в ответе. Получено: {body}"

    expected_error = "This field is required."
    assert expected_error in body["username"], \
        f"Ожидалась ошибка 'поле обязательно' ('{expected_error}'), получен список ошибок: {body['username']}"
