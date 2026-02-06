"""
Общие фикстуры pytest.
Тесты дергают API по HTTP (Docker: postgres + app). API_BASE_URL и БД — из .env в корне.
"""


from collections.abc import Generator

import pytest
import psycopg2

from clients.users_client import UsersClient
from config.settings import Settings, get_settings
from db.queries import UsersQueries
from models.user import UserResponse
from data.user_factory import get_single_user


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    """URL поднятого в Docker API (например http://localhost:3000)."""
    url = settings.api_base_url
    if not url:
        pytest.fail("API_BASE_URL is not set in environment")
    return url


@pytest.fixture(scope="session")
def api_client(base_url: str) -> UsersClient:
    """HTTP-клиент к API. Сервер должен быть поднят (docker compose up)."""
    return UsersClient(base_url)


@pytest.fixture(scope="session")
def db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """Подключение к PostgreSQL (для cleanup и тестов, смотрящих в БД)."""
    s = get_settings()
    try:
        with psycopg2.connect(
                host=s.db_host,
                port=s.db_port,
                dbname=s.db_name,
                user=s.db_user,
                password=s.db_password,
        ) as connection:
            yield connection
    except Exception as exc:
        pytest.fail(f"Could not connect to database: {exc}")


@pytest.fixture(scope="function")
def users_queries(db_connection: psycopg2.extensions.connection) -> UsersQueries:
    return UsersQueries(db_connection)


@pytest.fixture(scope="function")
def created_user(
        api_client: UsersClient,
        users_queries: UsersQueries,
) -> Generator[UserResponse, None, None]:
    """Создаёт пользователя через API, после теста удаляет через БД."""
    # Генерируем данные пользователя с помощью фабрики
    payload = get_single_user()
    # Убедимся, что email уникален, добавив временную метку
    payload["email"] = f"test_{abs(hash(str(id(payload)))) % 10000}@example.com"
    response = api_client.create_user(payload)
    response.raise_for_status()
    data = response.json()
    if not data:
        pytest.fail("create_user returned empty response body")
    user = UserResponse(**data)
    if not user.id:
        pytest.fail("User id is missing in create_user response")
    yield user
    users_queries.delete_user_by_id(user.id)
