# API Автотесты

Пет-проект **Senior AQA Python**: REST API на FastAPI + автотесты (pytest, requests, pydantic).  
API предоставляет CRUD операции для пользователей; тесты взаимодействуют с API через HTTP-клиенты и при необходимости очищают данные через прямое подключение к PostgreSQL.

---

## Стек

| Роль                | Технология                     |
| ------------------- | ------------------------------ |
| API                 | **FastAPI**, uvicorn           |
| БД                  | **PostgreSQL 15**              |
| Конфиг              | **pydantic-settings** (.env)   |
| Тесты               | **pytest**, requests, pydantic |
| Контейнеры          | **Docker**, docker-compose     |
| Генерация данных    | **Faker**                      |
| Документация тестов | **Markdown**                   |
| Линтер              | **Ruff**                       |
| Форматер            | **Ruff**                       |

---

## Структура проекта

```
api-autotests/
├── .env                    # Переменные для тестов (pydantic-settings, из корня)
├── pyproject.toml          # Зависимости, pytest, ruff
├── data/                   # Фабрики тестовых данных
│   └── user_factory.py     # Генератор пользовательских данных
├── docs/                   # Документация
│   ├── api_specification/  # Спецификация API
│   └── test_cases/         # Каталог с тест-кейсами
│       └── user/           # Тест-кейсы для пользовательских операций
├── src/
│   ├── app/                 # FastAPI-приложение (API)
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
        └── 001_create_users.sql  # Создание таблицы users при старте postgres (с расширенными полями)
```

---

## API Эндпоинты

API предоставляет полный CRUD функционал для пользователей с основными полями:

- `GET    /users/{id}` — Получить пользователя (включая поля: email, name, created_at, phone, address, birth_date)
- `POST   /users` — Создать пользователя (поддерживает дополнительные поля: name, phone, address, birth_date)
- `PUT    /users/{id}` — Полное обновление пользователя (все поля)
- `PATCH  /users/{id}` — Частичное обновление пользователя (любое подмножество полей)
- `DELETE /users/{id}` — Удалить пользователя

---

## Запуск

### 1. Переменные окружения

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

### 2. Запуск API и БД (Docker)

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

### 3. Запуск тестов

Поднимите в Docker и БД, и API: `docker compose up -d` (из каталога `docker/`). В `.env` в корне задайте `API_BASE_URL=http://localhost:3000` и параметры БД. Тесты вызывают API по HTTP.

Из **корня проекта**:

```bash
uv run pytest tests/ -v
```

Или с указанием файла/маркера:

```bash
uv run pytest tests/api/test_users_unit.py -v
```

---

## Требования

- Python 3.14+ (указано в `.python-version` / pyproject.toml)
- [uv](https://github.com/astral-sh/uv) для установки зависимостей и запуска (`uv sync`, `uv run pytest ...`)
- Docker и docker-compose для запуска API и PostgreSQL

## Документация

- **API Спецификация**: `docs/api_specification/API_Specification.md` - подробное описание всех endpoint'ов и структур данных
- **Руководство для новых пользователей**: `docs/api_specification/User_Guide.md` - пошаговая инструкция по началу работы с проектом

## Тестирование

Проект ориентирован на **интеграционное тестирование API**, поскольку:

- Бизнес-логика минимальна и сосредоточена на уровне БД
- Unit-тесты не обеспечивают значительной ценности по сравнению с end-to-end проверками
- Основная проверка функциональности происходит через HTTP-запросы к API
