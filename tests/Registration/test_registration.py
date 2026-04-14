import requests
import pytest
from jsonschema import validate
from schemas.registration_schema import payload_schema, error_username_already_exists_schema, \
    error_password_validation_schema, error_password_required_schema, error_username_validation_schema, \
    error_username_required

BASE_URL = "https://book-club.qa.guru/api/v1/users/register/"



def test_register_user_success(registration_data):
    """Тест успешной регистрации."""
    response = requests.post(f"{BASE_URL}", json=registration_data)

    print("\n--- УСПЕШНАЯ Регистрация ---")
    print("Status:", response.status_code)

    assert response.status_code == 201
    body = response.json()
    validate(instance=body, schema=payload_schema)
    assert "id" in body


def test_register_user_existing_username(existing_user_data):
    """Тест регистрации с уже существующим username."""

    response = requests.post(f"{BASE_URL}", json=existing_user_data)

    print("\n--- Регистрация существующего пользователя ---")
    print("Status:", response.status_code)

    assert response.status_code == 400  # Conflict
    body = response.json()
    validate(instance=body, schema=error_username_already_exists_schema)
    assert "username" in body and isinstance(body["username"], list), "Ответ не содержит массив ошибок для username"

    # Проверяем, что нужное сообщение есть в списке ошибок
    expected_error = "A user with that username already exists."
    assert expected_error in body["username"], f"Ожидалась ошибка '{expected_error}', получена {body['username']}"


def test_register_user_invalid_password(invalid_password_data):
    """Тест регистрации с пустым паролем."""

    response = requests.post(f"{BASE_URL}", json=invalid_password_data)

    print("\n--- Регистрация с невалидным паролем ---")
    print("Status:", response.status_code)
    print("Body:", response.text)  # Выведем тело для отладки

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    body = response.json()
    validate(instance=body, schema=error_password_validation_schema)

    assert "password" in body, f"Ключ 'password' отсутствует в ответе. Получено: {body}"
    assert isinstance(body["password"], list), "Значение ошибки должно быть списком"
    expected_error = "This field may not be blank."
    assert expected_error in body["password"], f"Ожидалась ошибка '{expected_error}', получена {body['password']}"


def test_register_user_missing_fields(missing_field_data):
        """Тест регистрации с отсутствующими параметром пароля."""
        response = requests.post(f"{BASE_URL}", json=missing_field_data)

        print("\n--- Регистрация с отсутствующим параметром пароля ---")
        print("Status:", response.status_code)

        assert response.status_code == 400  # Bad Request
        body = response.json()
        validate(instance=body, schema=error_password_required_schema)

        assert "password" in body, f"Ключ 'password' отсутствует в ответе. Получено: {body}"
        assert isinstance(body["password"], list), "Значение ошибки должно быть списком"
        expected_error = "This field is required."
        assert expected_error in body["password"], f"Ожидалась ошибка '{expected_error}', получена {body['password']}"


def test_register_user_empty_username(empty_username_data):
    """Тест регистрации с пустым полем username."""
    response = requests.post(f"{BASE_URL}", json=empty_username_data)

    print("\n--- Регистрация с пустым username ---")
    print("Status:", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_username_validation_schema)
    # Ожидаем, что сервер вернет ошибку именно для поля username
    assert "username" in body, f"Ключ 'username' отсутствует в ответе. Получено: {body}"

    expected_error = "This field may not be blank."
    assert expected_error in body["username"], f"Ожидалась ошибка про пустое поле, получена: {body['username']}"


def test_register_user_missing_username(missing_username_data):
    """Тест регистрации с отсутствующим параметром username."""
    response = requests.post(f"{BASE_URL}", json=missing_username_data)

    print("\n--- Регистрация с отсутствующим username ---")
    print("Status:", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_username_required)
    # Ожидаем, что сервер сообщит об отсутствии поля username
    assert "username" in body, f"Ключ 'username' отсутствует в ответе. Получено: {body}"

    expected_error = "This field is required."
    assert expected_error in body["username"], f"Ожидалась ошибка 'поле обязательно', получена: {body['username']}"