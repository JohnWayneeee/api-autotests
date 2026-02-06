"""
Прямые SQL-запросы к таблице users.
Используются в тестах для проверки данных в БД и для cleanup (удаление после теста).
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional


class UsersQueries:
    """Обёртка над psycopg2: выборка и удаление по id. Курсор RealDictCursor — строки как dict."""

    def __init__(self, connection):
        """connection — уже открытое psycopg2-подключение (из фикстуры db_connection)."""
        self.connection = connection

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Выбрать одну запись из users по id. Возвращает dict или None."""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, email, name, created_at, phone, address, birth_date FROM users WHERE id = %s;",
                (user_id,),
            )
            return cursor.fetchone()

    def delete_user_by_id(self, user_id: int) -> None:
        """Удалить запись из users по id. Commit делается здесь (автокоммит не используем)."""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s;",
                (user_id,),
            )
            self.connection.commit()
