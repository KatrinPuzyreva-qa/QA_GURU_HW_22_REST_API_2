import pytest
import random
from faker import Faker

fake = Faker()

@pytest.fixture
def registration_data():
    """
    Валидные данные для регистрации нового пользователя.
    Использует Faker и модуль random для генерации уникального username.
    """
    # Используем глобально импортированный модуль random
    unique_suffix = random.randint(100, 999)

    return {
        "username": f"{fake.user_name()}_{unique_suffix}",
        "password": "StrongP@ssw0rd123"
    }

@pytest.fixture
def existing_user_data():
    """Возвращает данные пользователя, который заведомо существует в системе."""
    return {
        "username": "testuser",  # Имя пользователя, которое уже есть в БД
        "password": "SomePassword123"
    }

@pytest.fixture
def invalid_password_data(registration_data):
    """Данные с невалидным (пустым) паролем."""
    data = registration_data.copy()
    data["password"] = ""  # Нарушение: пустой пароль
    return data

@pytest.fixture
def missing_field_data():
    """Данные с отсутствующим обязательным полем 'password'."""
    return {
        "username": "user_without_password"
        # Поле password отсутствует намеренно
    }

@pytest.fixture
def empty_username_data(registration_data):
    """Данные с пустым полем username."""
    data = registration_data.copy()
    data["username"] = ""  # Нарушение: пустое имя пользователя
    return data

@pytest.fixture
def missing_username_data():
    """Данные с отсутствующим полем username."""
    return {
        "password": "SomePassword123"
        # Поле username отсутствует намеренно
    }
