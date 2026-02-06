"""
Базовый HTTP-клиент для вызова API из автотестов.
Используется при запуске тестов против поднятого в Docker сервера (API + БД).
"""

import requests


class BaseApiClient:
    """Обёртка над requests: GET, POST, DELETE к API по base_url."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _get(self, path: str, params: dict | None = None) -> requests.Response:
        return self.session.get(url=f"{self.base_url}{path}", params=params)

    def _post(self, path: str, json: dict) -> requests.Response:
        return self.session.post(url=f"{self.base_url}{path}", json=json)

    def _delete(self, path: str) -> requests.Response:
        return self.session.delete(url=f"{self.base_url}{path}")

    def _put(self, path: str, json: dict) -> requests.Response:
        return self.session.put(url=f"{self.base_url}{path}", json=json)

    def _patch(self, path: str, json: dict) -> requests.Response:
        return self.session.patch(url=f"{self.base_url}{path}", json=json)
