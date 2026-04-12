import pytest
from faker import Faker

fake = Faker()

# Фикстура для успешного теста (рандомные данные)
@pytest.fixture
def registration_data():
    """Фикстура для успешного теста (рандомные данные)."""
    username = fake.user_name()
    password = fake.password(length=9)

    print(f"\n--- Данные для регистрации (логин/пароль) ---")
    print(f"Username: {username}")
    print(f"Password: {password}")

    return {"username": username, "password": password}

# Фикстура для теста с существующим пользователем
# Используем статичные данные, чтобы мы точно знали, что они уже заняты
@pytest.fixture
def existing_user_data():
    return {"username": "existing_user_123", "password": "StrongPass!1"}

# Фикстура для теста с невалидным паролем
@pytest.fixture
def invalid_password_data():
    return {"username": fake.user_name(), "password": ""} # Пустой пароль

# Фикстура для теста с отсутствующими полями
@pytest.fixture
def missing_field_data():
    return {"username": fake.user_name()} # Пароль отсутствует

# Фикстура для теста с пустым полем username
@pytest.fixture
def empty_username_data():
    password = fake.password(length=12, special_chars=False)
    return {"username": "", "password": password}

# Новая фикстура: отсутствующий параметр username
@pytest.fixture
def missing_username_data():
    """Фикстура для теста с отсутствующим полем username."""
    # В словаре нет ключа 'username'
    return {"password": fake.password(length=12, special_chars=False)}