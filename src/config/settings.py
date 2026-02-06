"""
Конфиг приложения и тестов — один источник правды.
Читает переменные из .env и окружения, валидирует при загрузке (pydantic-settings).
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки из env. При отсутствии переменной подставляется дефолт ниже.
    Имена полей в lowercase — в env ищутся как UPPER_SNAKE (api_base_url → API_BASE_URL).
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",  # Файл в корне проекта (или от cwd)
        env_file_encoding="utf-8",
        extra="ignore",  # Не падать на лишние переменные в .env
    )
    
    # URL, на который тесты шлют запросы (тот же, что слушает FastAPI)
    api_base_url: str = Field(
        default="http://localhost:3000",
        description="Base URL API для тестов",
    )
    # Параметры подключения к PostgreSQL (для приложения и для тестовой очистки данных)
    db_host: str = Field(default="localhost", description="PostgreSQL host")
    db_port: int = Field(default=5432, ge=1, le=65535, description="PostgreSQL port")
    db_name: str = Field(default="api", description="PostgreSQL database name")
    db_user: str = Field(default="api_user", description="PostgreSQL user")
    db_password: str = Field(default="api_pass", description="PostgreSQL password")


@lru_cache
def get_settings() -> Settings:
    """Синглтон настроек: один раз загружаем из env, дальше из кэша."""
    return Settings()


# Алиасы для обратной совместимости: from config.settings import API_BASE_URL, DB_HOST, ...
_settings = get_settings()
API_BASE_URL = _settings.api_base_url
DB_HOST = _settings.db_host
DB_PORT = _settings.db_port
DB_NAME = _settings.db_name
DB_USER = _settings.db_user
DB_PASSWORD = _settings.db_password
