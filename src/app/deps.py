"""
Зависимости приложения: подключение к PostgreSQL.
Конфиг берётся из config.settings (один источник правды).
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from src.config.settings import get_settings


def get_db_config() -> dict:
    """Словарь параметров для psycopg2.connect (host, port, dbname, user, password)."""
    s = get_settings()
    return {
        "host": s.db_host,
        "port": s.db_port,
        "dbname": s.db_name,
        "user": s.db_user,
        "password": s.db_password,
    }


@contextmanager
def get_db_connection():
    """
    Контекстный менеджер: открывает соединение, по выходу закрывает.
    Использование: with get_db_connection() as conn: ...
    """
    conn = psycopg2.connect(**get_db_config())
    try:
        yield conn
    finally:
        conn.close()


def get_db_cursor(conn):
    """Курсор с RealDictCursor — каждая строка как dict (ключи — имена колонок)."""
    return conn.cursor(cursor_factory=RealDictCursor)
