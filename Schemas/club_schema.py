success_create_club = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "id": {
      "type": "number"
    },
    "bookTitle": {
      "type": "string"
    },
    "bookAuthors": {
      "type": "string"
    },
    "publicationYear": {
      "type": "number"
    },
    "description": {
      "type": "string"
    },
    "telegramChatLink": {
      "type": "string"
    },
    "owner": {
      "type": "number"
    },
    "members": {
      "type": "array",
      "items": {
        "type": "number"
      }
    },
    "reviews": {
      "type": "array",
      "items": {}
    },
    "created": {
      "type": "string"
    },
    "modified": {}
  },
  "required": [
    "id",
    "bookTitle",
    "bookAuthors",
    "publicationYear",
    "description",
    "telegramChatLink",
    "owner",
    "members",
    "reviews",
    "created",
    "modified"
  ]
}

club_detail_schema_patch = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "title": "Детальная информация о клубе",
  "description": "Схема объекта, возвращаемого при запросе информации о конкретном клубе.",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Уникальный идентификатор клуба в системе.",
      "example": 886
    },
    "bookTitle": {
      "type": "string",
      "description": "Название книги, которую обсуждают в клубе.",
      "example": "booking_info"
    },
    "bookAuthors": {
      "type": "string",
      "description": "Автор(ы) книги.",
      "example": "booking_author"
    },
    "publicationYear": {
      "type": "integer",
      "description": "Год публикации книги.",
      "example": 2147483647
    },
    "description": {
      "type": "string",
      "description": "Описание клуба или темы обсуждения.",
      "example": "description"
    },
    "telegramChatLink": {
      "type": "string",
      "description": "Ссылка на чат клуба в Telegram.",
      "format": "uri",
      "example": "https://t.me/qa.guru"
    },
    "owner": {
      "type": "integer",
      "description": "ID пользователя, создавшего клуб.",
      "example": 1772
    },
    "members": {
      "type": "array",
      "description": "Список ID пользователей, состоящих в клубе.",
      "items": {
        "type": "integer"
      },
      "example": [1772]
    },
    "reviews": {
      "type": "array",
      "description": "Список объектов-отзывов о клубе.",
      "items": {
        "type": "object"
      },
      "example": []
    },
    "created": {
      "type": "string",
      "description": "Дата и время создания клуба.",
      "format": "date-time",
      "example": "2026-04-12T13:24:56.977446Z"
    },
      "modified": {
      "description": "Дата и время последнего изменения клуба. Может быть null.",
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "example": None
    }
  },
}