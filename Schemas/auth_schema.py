from Schemas.registration_schema import error_password_required_schema

success_auth = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "refresh": {
      "type": "string"
    },
    "access": {
      "type": "string"
    }
  },
  "required": [
    "refresh",
    "access"
  ]
}

base_error_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "detail": {
      "type": "string"
    }
  },
  "required": [
    "detail"
  ]
}

error_password_required_schema_auth = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда обязательное поле 'password' отсутствует в запросе.",
  "properties": {
    "password": {
      "type": "array",
      "description": "Список сообщений об ошибках для поля пароля.",
      "items": {
        "type": "string",
        "description": "Текст сообщения об ошибке."
      },
      "minItems": 1,
      "example": ["This field is required."]
    }
  },
  "required": ["password"],
  "additionalProperties": False
}

error_username_required_schema_auth ={
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда обязательное поле 'username' отсутствует в запросе.",
  "properties": {
    "username": {
      "type": "array",
      "description": "Список сообщений об ошибках для поля логина.",
      "items": {
        "type": "string",
        "description": "Текст сообщения об ошибке."
      },
      "minItems": 1,
      "example": ["This field is required."]
    }
  },
  "required": ["username"],
  "additionalProperties": False
}


error_username_and_password_required = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда обязательные поля 'username' и 'password' отсутствуют в запросе.",
  "properties": {
    "username": {
      "type": "array",
      "description": "Список сообщений об ошибках для поля логина.",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "password": {
      "type": "array",
      "description": "Список сообщений об ошибках для поля пароля.",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  },
  "required": ["username", "password"],
  "additionalProperties": False
}
wrong_credentials_auth = base_error_schema
unsupported_media_type = base_error_schema