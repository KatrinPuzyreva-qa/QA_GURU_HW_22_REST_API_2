import pytest

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "katrin"
PASSWORD = "katrin1"
TOKEN_PATH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
CLUB_ID = 886
PATCH_PAYLOAD = {
    "bookTitle": "booking_info",
    "bookAuthors": "booking_author",
    "publicationYear": 2147483647,
    "description": "description",
    "telegramChatLink": "https://t.me/qa.guru"
}

@pytest.fixture
def valid_credentials():
    """Возвращает словарь с валидными логином и паролем."""
    return {"username": USERNAME, "password": PASSWORD}

@pytest.fixture
def wrong_password_data():
    """Возвращает словарь с валидным логином и невалидным паролем."""
    return {"username": USERNAME, "password": "wrong"}

@pytest.fixture
def missing_password_data():
    """Возвращает словарь с отсутствующим паролем."""
    return {"username": USERNAME}

@pytest.fixture
def missing_username_data():
    """Возвращает словарь с отсутствующим логином."""
    return {"password": PASSWORD}

@pytest.fixture
def missing_both_data():
    """Возвращает пустой словарь (отсутствуют оба поля)."""
    return {}

# Фикстура для "мусорных" типов тела (вы уже ее сделали)
@pytest.fixture(params=[None, True, 123, "just a text", []])
def wrong_body_type_data(request):
    """Фикстура для тестов с некорректным типом тела запроса."""
    return request.param

# Фикстура для заголовков с неправильным Content-Type
@pytest.fixture
def png_headers():
    """Возвращает заголовки для запроса с типом image/png."""
    return {"content-type": "image/png"}

@pytest.fixture(params=[None, True, 123, "just a text", []])
def wrong_body_type_data(request):
    return request.param

#Эта фикстура позволит запустить тест 5 раз (по количеству элементов в `params`),