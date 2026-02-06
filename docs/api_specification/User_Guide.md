# Инструкция для новых пользователей

## Обзор проекта

Этот проект представляет собой пет-проект для Senior AQA Python, включающий REST API на FastAPI и автотесты на pytest, requests и pydantic. API предоставляет полный CRUD функционал для пользователей, а тесты взаимодействуют с API через HTTP-клиенты.

## Стек технологий

| Компонент        | Технология                     |
| ---------------- | ------------------------------ |
| API              | **FastAPI**, uvicorn           |
| БД               | **PostgreSQL 15**              |
| Конфиг           | **pydantic-settings** (.env)   |
| Тесты            | **pytest**, requests, pydantic |
| Контейнеры       | **Docker**, docker-compose     |
| Генерация данных | **Faker**                      |
| Документация     | **Markdown**                   |

## Структура проекта

```
api-autotests/
├── .env                    # Переменные для тестов (pydantic-settings, из корня)
├── pyproject.toml          # Зависимости, pytest, ruff
├── data/                   # Фабрики тестовых данных
│   └── user_factory.py     # Генератор пользовательских данных
├── docs/                   # Документация
│   ├── api_specification/  # Спецификация API
│   │   ├── API_Specification.md  # Общая спецификация API
│   │   └── User_Guide.md         # Настоящий файл (инструкция для новых пользователей)
│   └── test_cases/         # Каталог с тест-кейсами
│       └── user/           # Тест-кейсы для пользовательских операций
├── src/
│   ├── app/                # FastAPI-приложение (API)
│   │   ├── main.py         # Точка входа, подключение роутеров
│   │   ├── deps.py         # Подключение к PostgreSQL (конфиг из settings)
│   │   ├── schemas.py      # Request-схемы (UserCreate и т.д.)
│   │   └── routers/
│   │       └── users.py    # Эндпоинты GET/POST/PUT/PATCH/DELETE /users
│   ├── clients/            # HTTP-клиенты для тестов (вызов API по URL)
│   │   ├── api_client.py   # Базовый HTTP клиент
│   │   └── users_client.py # Клиент для работы с пользователями (GET/POST/PUT/PATCH/DELETE)
│   ├── config/
│   │   └── settings.py     # Настройки из .env (pydantic-settings)
│   ├── db/
│   │   └── queries.py      # SQL-запросы к users (для тестов и cleanup)
│   └── models/
│       └── user.py        # Модель ответа UserResponse (1:1 с таблицей users)
├── tests/
│   ├── conftest.py        # Фикстуры: base_url, api_client, db_connection, created_user
│   └── api/               # Тесты для пользовательского API
└── docker/
    ├── .env                # Переменные для Docker (Compose ищет здесь)
    ├── docker-compose.yaml # postgres, app (FastAPI), adminer
    ├── Dockerfile          # Сборка образа приложения
    └── init/
        └── 001_create_users.sql  # Создание таблицы users при старте postgres
```

## Как запустить проект

### 1. Предварительные требования

- Python 3.14+ (указано в `.python-version` / pyproject.toml)
- [uv](https://github.com/astral-sh/uv) для установки зависимостей и запуска (`uv sync`, `uv run pytest ...`)
- Docker и docker-compose для запуска API и PostgreSQL

### 2. Установка зависимостей

```bash
# Установка uv (если еще не установлен)
pip install uv

# Установка зависимостей проекта
uv sync
```

### 3. Настройка переменных окружения

**Для Docker** — Compose ищет `.env` в каталоге с `docker-compose.yaml`. Создайте файл **`docker/.env`** (или скопируйте `.env` из корня в `docker/`):

```env
POSTGRES_USER=api_user
POSTGRES_PASSWORD=api_pass
POSTGRES_DB=api
DB_HOST=postgres
DB_PORT=5432
DB_NAME=api
DB_USER=api_user
DB_PASSWORD=api_pass
API_BASE_URL=http://localhost:3000
```

**Для тестов (pytest)** — настройки читаются из `.env` в **корне проекта** (pydantic-settings). Там же задайте `API_BASE_URL` и параметры БД; для локального запуска тестов `DB_HOST=localhost`.

### 4. Запуск API и БД (Docker)

Перейдите в каталог `docker/` и поднимите сервисы:

```bash
cd docker
docker compose up -d --build
```

Либо из корня проекта:

```bash
docker compose -f docker/docker-compose.yaml up -d --build
```

В обоих случаях `.env` должен лежать в **`docker/`** (рядом с `docker-compose.yaml`).

- API: http://localhost:3000
- Adminer (БД): http://localhost:8080

Остановка: `docker compose down -v` (из каталога `docker/`) или `docker compose -f docker/docker-compose.yaml down -v` (из корня).

### 5. Запуск тестов

Поднимите в Docker и БД, и API: `docker compose up -d` (из каталога `docker/`). В `.env` в корне задайте `API_BASE_URL=http://localhost:3000` и параметры БД. Тесты вызывают API по HTTP.

Из **корня проекта**:

```bash
uv run pytest tests/ -v
```

Или с указанием файла/маркера:

```bash
uv run pytest tests/api/test_users_unit.py -v
```

## Как писать тесты

### Использование фабрики данных

Для генерации тестовых данных используется фабрика в `data/user_factory.py`:

```python
from data.user_factory import get_single_user, get_multiple_users

# Генерация одного пользователя со всеми полями
user_data = get_single_user()

# Генерация одного пользователя только с обязательными полями
user_data = get_single_user(include_optional_fields=False)

# Генерация нескольких пользователей
users_data = get_multiple_users(count=3)

# Генерация пользователя с переопределенным email
user_data = get_single_user(email="custom@example.com")
```

### Использование HTTP-клиента

Для взаимодействия с API используйте клиент из `src/clients/users_client.py`:

```python
from src.clients.users_client import UsersClient
from src.config.settings import get_settings

settings = get_settings()
client = UsersClient(settings.api_base_url)

# Создание пользователя
response = client.create_user({"email": "test@example.com", "name": "Test User"})

# Получение пользователя
response = client.get_user(1)

# Обновление пользователя
response = client.update_user(1, {"email": "updated@example.com", "name": "Updated User"})

# Частичное обновление пользователя
response = client.partial_update_user(1, {"name": "Partially Updated User"})

# Удаление пользователя
response = client.delete_user(1)
```

### Использование фикстур

В `tests/conftest.py` определены следующие фикстуры:

- `settings` - объект настроек
- `base_url` - URL поднятого в Docker API
- `api_client` - HTTP-клиент к API
- `db_connection` - Подключение к PostgreSQL
- `users_queries` - Клиент для работы с БД
- `created_user` - Фикстура, создающая пользователя через API и удаляющая его после теста

Пример использования фикстур в тесте:

```python
def test_create_user(api_client):
    payload = get_single_user()
    response = api_client.create_user(payload)
    assert response.status_code == 201

    user_data = response.json()
    assert user_data["email"] == payload["email"]
```

## Рекомендации по работе с проектом

### Создание новых тестов

1. Размещайте новые тесты в соответствующих подкаталогах `tests/api/`
2. Используйте фабрику данных для генерации тестовых данных
3. Используйте фикстуры из `conftest.py` для получения клиента API и других необходимых объектов
4. Следите за тем, чтобы тесты были независимы друг от друга
5. Используйте подходящие уровни детализации: unit-тесты для проверки отдельных функций, интеграционные тесты для проверки взаимодействия компонентов

### Структура тест-кейсов

Тест-кейсы находятся в `docs/test_cases/user/` и имеют следующую структуру:

- TC_API_USERS_CREATE_POS_001.md - Создание пользователя (позитивный кейс)
- TC_API_USERS_GET_BY_ID_POS_002.md - Получение пользователя по ID (позитивный кейс)
- TC_API_USERS_UPDATE_PUT_POS_003.md - Обновление пользователя (позитивный кейс)
- TC_API_USERS_PARTIAL_UPDATE_PATCH_POS_004.md - Частичное обновление пользователя (позитивный кейс)
- TC_API_USERS_DELETE_POS_005.md - Удаление пользователя (позитивный кейс)
- TC_API_USERS_CREATE_NEG_006.md - Создание пользователя (негативный кейс)
- TC_API_USERS_GET_BY_ID_NEG_007.md - Получение пользователя по ID (негативный кейс)
- TC_API_USERS_UPDATE_NEG_008.md - Обновление пользователя (негативный кейс)

### Работа с полями пользователя

Текущая схема пользователя включает следующие поля:

- `id` (integer, обязательное) - Primary key, SERIAL
- `email` (string, обязательное, max_length=255) - Email, NOT NULL UNIQUE
- `name` (string | null, опциональное, min_length=1, max_length=100) - Имя, nullable
- `created_at` (datetime, обязательное) - Created at, TIMESTAMP DEFAULT now()
- `phone` (string | null, опциональное, max_length=20) - Номер телефона, nullable
- `address` (string | null, опциональное, max_length=255) - Адрес, nullable
- `birth_date` (datetime | null, опциональное) - Дата рождения, nullable

### Основные endpoint'ы

- `GET    /users/{id}` — Получить пользователя
- `POST   /users` — Создать пользователя
- `PUT    /users/{id}` — Полное обновление пользователя
- `PATCH  /users/{id}` — Частичное обновление пользователя
- `DELETE /users/{id}` — Удалить пользователя

## Заключение

Этот проект готов для практики API-тестирования и CI. Архитектура позволяет легко добавлять новые тесты и расширять функциональность. Все компоненты системы согласованы и готовы к использованию.
