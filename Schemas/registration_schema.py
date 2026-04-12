payload_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "Ответ при успешной регистрации пользователя",
  "description": "Схема объекта, возвращаемого API после создания нового пользователя",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Уникальный идентификатор пользователя в системе",
      "example": 1774
    },
    "username": {
      "type": "string",
      "description": "Уникальное имя пользователя (логин)",
      "example": "katrin2"
    },
    "firstName": {
      "type": "string",
      "description": "Имя пользователя",
      "example": ""
    },
    "lastName": {
      "type": "string",
      "description": "Фамилия пользователя",
      "example": ""
    },
    "email": {
      "type": "string",
      "description": "Адрес электронной почты пользователя",
      "example": ""
    },
    "remoteAddr": {
      "type": "string",
      "description": "IP-адрес, с которого был выполнен запрос",
      "format": "ipv4",
      "example": "93.77.180.175"
    }
  },
  "required": ["id", "username", "remoteAddr"],
  "additionalProperties": False
}



error_username_already_exists_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке при попытке регистрации существующего пользователя",
  "properties": {
    "username": {
      "type": "array",
      "description": "Список сообщений об ошибках, связанных с полем username",
      "items": {
        "type": "string",
        "description": "Текст ошибки"
      },
      "minItems": 1,
      "example": ["A user with that username already exists."]
    }
  },
  "required": ["username"],
  "additionalProperties": False
}

error_password_validation_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда поле пароля не заполнено или некорректно",
  "properties": {
    "password": {
      "type": "array",
      "description": "Список сообщений об ошибках, связанных с полем пароля",
      "items": {
        "type": "string",
        "description": "Текст ошибки валидации"
      },
      "minItems": 1
    }
  },
  "required": ["password"],
  "additionalProperties": False
}

error_password_required_schema = {
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

error_username_validation_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда поле username не заполнено или содержит некорректное значение.",
  "properties": {
    "username": {
      "type": "array",
      "description": "Список сообщений об ошибках, связанных с полем username.",
      "items": {
        "type": "string",
        "description": "Текст сообщения об ошибке валидации."
      },
      "minItems": 1,
      "example": ["This field may not be blank."]
    }
  },
  "required": ["username"],
  "additionalProperties": False
}

error_username_required = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "description": "Схема ответа об ошибке валидации, когда обязательное поле 'username' отсутствует в запросе.",
  "properties": {
    "username": {
      "type": "array",
      "description": "Список сообщений об ошибках для поля username.",
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