"""
Модель ответа API по пользователю — 1:1 с таблицей users (docker/init/001_create_users.sql).
Используется в тестах для парсинга ответа и в FastAPI для response_model.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserResponse(BaseModel):
    """Одна запись из users: id, email, name, created_at и другие поля."""

    id: int = Field(..., description="Primary key, SERIAL")
    email: EmailStr = Field(..., max_length=255,
                            description="Email, NOT NULL UNIQUE")
    name: str | None = Field(
        None, min_length=1, max_length=100, description="Name, nullable")
    created_at: datetime = Field(...,
                                 description="Created at, TIMESTAMP DEFAULT now()")
    phone: str | None = Field(
        None, max_length=20, description="Phone number, nullable")
    address: str | None = Field(
        None, max_length=255, description="Address, nullable")
    birth_date: datetime | None = Field(
        None, description="Birth date, nullable")
