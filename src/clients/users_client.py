"""
HTTP-клиент к эндпоинтам /users. Для тестов против поднятого в Docker API.
"""

from .api_client import BaseApiClient


class UsersClient(BaseApiClient):
    """GET /users/{id}, POST /users, PUT /users/{id}, PATCH /users/{id}, DELETE /users/{id}."""

    def create_user(self, payload: dict):
        """POST /users — создание пользователя. payload: { email, name?, phone?, address?, birth_date? }."""
        return self._post("/users", json=payload)

    def get_user(self, user_id: int):
        """GET /users/{user_id} — получить пользователя по id."""
        return self._get(f"/users/{user_id}")

    def update_user(self, user_id: int, payload: dict):
        """PUT /users/{user_id} — полное обновление пользователя."""
        return self._put(f"/users/{user_id}", json=payload)

    def partial_update_user(self, user_id: int, payload: dict):
        """PATCH /users/{user_id} — частичное обновление пользователя."""
        return self._patch(f"/users/{user_id}", json=payload)

    def delete_user(self, user_id: int):
        """DELETE /users/{user_id} — удалить пользователя по id."""
        return self._delete(f"/users/{user_id}")
