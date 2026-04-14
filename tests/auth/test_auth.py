import requests
from jsonschema import validate
from schemas.auth_schema import success_auth, wrong_credentials_auth, unsupported_media_type, \
    error_password_required_schema_auth, error_username_required_schema_auth, error_username_and_password_required
from tests.auth.conftest import wrong_body_type_data, API_URL, TOKEN_PATH, valid_credentials


def test_successful_auth(valid_credentials):
    """Тест успешной авторизации."""
    response = requests.post(API_URL + "/auth/token/", json=valid_credentials)

    print(
        f"--- УСПЕШНАЯ Авторизация ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Headers: {response.headers}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_auth)

    access_token = body["access"]
    refresh_token = body["refresh"]

    # Проверки токенов
    assert TOKEN_PATH in access_token
    assert TOKEN_PATH in refresh_token
    assert len(access_token.split(".")) == 3, "Токен должен состоять из 3 частей, разделенных точкой"
    assert len(refresh_token.split(".")) == 3, "Токен должен состоять из 3 частей, разделенных точкой"
    assert access_token != refresh_token, "Access и Refresh токены не должны совпадать"


def test_wrong_credentials_auth(wrong_password_data):
    """Тест авторизации с неверным паролем."""
    response = requests.post(API_URL + "/auth/token/", json=wrong_password_data)

    print(
        f"--- Авторизация с неверным паролем ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."

def test_missing_password_auth(missing_password_data):
    """Тест авторизации с отсутствующим паролем."""
    response = requests.post(API_URL + "/auth/token/", json=missing_password_data)

    print(
        f"--- Авторизация без пароля ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_password_required_schema_auth)

    expected_error = "This field is required."
    assert expected_error in body["password"], f"Ожидалась ошибка '{expected_error}', получена: {body['password']}"


def test_wrong_content_type_auth(valid_credentials, png_headers):
    """Тест авторизации с неправильным заголовком Content-Type."""
    response = requests.post(API_URL + "/auth/token/", headers=png_headers, json=valid_credentials)

    print(
        f"--- Авторизация с неправильным заголовком Content-Type ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 415

    body = response.json()
    validate(body, schema=unsupported_media_type)

    assert body["detail"] == "Unsupported media type \"image/png\" in request."


def test_missing_username_auth(missing_username_data):
    """Тест авторизации с отсутствующим логином."""
    response = requests.post(API_URL + "/auth/token/", json=missing_username_data)

    print(
        f"--- Авторизация без логина ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 400

    body = response.json()
    validate(instance=body, schema=error_username_required_schema_auth)

    # Проверяем наличие ключа 'password' и текста ошибки внутри него
    assert "username" in body, f"Ключ 'username' отсутствует в ответе: {body}"

    expected_error = "This field is required."
    assert expected_error in body["username"], f"Ожидалась ошибка '{expected_error}', получена: {body['username']}"


def test_missing_username_and_password_auth(missing_both_data):
    """Тест авторизации с отсутствующими логином и паролем."""
    response = requests.post(API_URL + "/auth/token/", json=missing_both_data)

    print(
        f"--- Авторизация без логина и пароля ---\n"
        f"\nStatus: {response.status_code}\n"
        f"Body: {response.text}"
    )
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    body = response.json()
    validate(instance=body, schema=error_username_and_password_required)

    # Проверяем наличие всех ключей в ответе об ошибке
    assert "username" in body and "password" in body, \
            f"Ожидались ключи 'username' и 'password'. Получено: {body.keys()}"

    expected_error = "This field is required."

    # Проверяем текст ошибки для username
    assert expected_error in body["username"], \
            f"Ожидалась ошибка '{expected_error}' для username, получена: {body['username']}"

    # Проверяем текст ошибки для password
    assert expected_error in body["password"], \
            f"Ожидалась ошибка '{expected_error}' для password, получена: {body['password']}"


def test_wrong_body_type(wrong_body_type_data):
    #Тест авторизации с некорректным типом тела запроса.API корректно обрабатывает None, True, числа, строки и списки.
    #Фикстура запустит тест 5 раз с разными значениями.

    print(
        f"--- Авторизация с некорректным типом тела запроса ---\n"
        f"\nОтправляемое тело: {wrong_body_type_data}\n"
        )
    response = requests.post(API_URL + "/auth/token/", json=wrong_body_type_data)

    print("Status code:", response.status_code)
    print("Body:", response.text)

    # Проверяем, что сервер вернул ошибку клиента (4xx), а не упал с ошибкой 500
    assert response.status_code >= 400 and response.status_code < 500, \
            f"Ожидался код ошибки клиента (4xx), получен {response.status_code}"