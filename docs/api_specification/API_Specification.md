# API Спецификация

## Обзор

Этот документ описывает API для управления пользователями. API предоставляет полный CRUD функционал для пользователей с основными полями.

## Базовые поля пользователя

| Поле       | Тип              | Обязательное | Ограничения                  | Описание                            |
| ---------- | ---------------- | ------------ | ---------------------------- | ----------------------------------- |
| id         | integer          | Да           | -                            | Primary key, SERIAL                 |
| email      | string           | Да           | max_length=255               | Email, NOT NULL UNIQUE              |
| name       | string \| null   | Нет          | min_length=1, max_length=100 | Имя, nullable                       |
| created_at | datetime         | Да           | -                            | Created at, TIMESTAMP DEFAULT now() |
| phone      | string \| null   | Нет          | max_length=20                | Номер телефона, nullable            |
| address    | string \| null   | Нет          | max_length=255               | Адрес, nullable                     |
| birth_date | datetime \| null | Нет          | -                            | Дата рождения, nullable             |

## Endpoint'ы

### GET /users/{id}

Получение пользователя по ID.

#### Параметры

- **user_id** (path, integer, required) - ID пользователя

#### Ответы

- **200 OK** - Пользователь найден
  - Body: UserResponse
- **404 Not Found** - Пользователь не найден

### POST /users

Создание нового пользователя.

#### Тело запроса

- **email** (string, required) - Email пользователя
- **name** (string, optional) - Имя пользователя
- **phone** (string, optional) - Номер телефона
- **address** (string, optional) - Адрес
- **birth_date** (datetime, optional) - Дата рождения

#### Ответы

- **201 Created** - Пользователь успешно создан
  - Body: UserResponse
- **409 Conflict** - Пользователь с таким email уже существует

### PUT /users/{id}

Полное обновление пользователя.

#### Параметры

- **user_id** (path, integer, required) - ID пользователя

#### Тело запроса

- **email** (string, required) - Email пользователя
- **name** (string, optional) - Имя пользователя
- **phone** (string, optional) - Номер телефона
- **address** (string, optional) - Адрес
- **birth_date** (datetime, optional) - Дата рождения

#### Ответы

- **200 OK** - Пользователь успешно обновлен
  - Body: UserResponse
- **404 Not Found** - Пользователь не найден

### PATCH /users/{id}

Частичное обновление пользователя.

#### Параметры

- **user_id** (path, integer, required) - ID пользователя

#### Тело запроса

- Любое подмножество полей:
  - **email** (string, optional) - Email пользователя
  - **name** (string, optional) - Имя пользователя
  - **phone** (string, optional) - Номер телефона
  - **address** (string, optional) - Адрес
  - **birth_date** (datetime, optional) - Дата рождения

#### Ответы

- **200 OK** - Пользователь успешно обновлен
  - Body: UserResponse
- **400 Bad Request** - Нет полей для обновления
- **404 Not Found** - Пользователь не найден

### DELETE /users/{id}

Удаление пользователя.

#### Параметры

- **user_id** (path, integer, required) - ID пользователя

#### Ответы

- **204 No Content** - Пользователь успешно удален
- **404 Not Found** - Пользователь не найден

## Структуры данных

### UserResponse

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T10:00:00",
  "phone": "+79991234567",
  "address": "ул. Примерная, д. 1",
  "birth_date": "1990-01-01"
}
```

### UserCreate

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+79991234567",
  "address": "ул. Примерная, д. 1",
  "birth_date": "1990-01-01"
}
```

### UserUpdate

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+79991234567",
  "address": "ул. Примерная, д. 1",
  "birth_date": "1990-01-01"
}
```

### UserPatch

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+79991234567",
  "address": "ул. Примерная, д. 1",
  "birth_date": "1990-01-01"
}
```

## Ошибки

| Код | Сообщение                           | Описание                                          |
| --- | ----------------------------------- | ------------------------------------------------- |
| 400 | No fields to update                 | При PATCH-запросе не переданы поля для обновления |
| 404 | User not found                      | Пользователь с указанным ID не найден             |
| 409 | User with this email already exists | Пользователь с таким email уже существует         |
