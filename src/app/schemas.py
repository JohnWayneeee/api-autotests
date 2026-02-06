"""
Request-схемы API: тело входящих запросов (POST и т.д.).
Валидация через Pydantic (например EmailStr для email).
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Тело POST /users — поля соответствуют колонкам в таблице users."""
    email: EmailStr = Field(..., max_length=255,
                            description="Email, NOT NULL UNIQUE в БД")
    name: str | None = Field(
        None, min_length=1, max_length=100, description="Name, nullable в БД")
    phone: str | None = Field(
        None, max_length=20, description="Phone number, nullable в БД")
    address: str | None = Field(
        None, max_length=255, description="Address, nullable в БД")
    birth_date: datetime | None = Field(
        None, description="Birth date, nullable в БД")


class UserUpdate(BaseModel):
    """Тело PUT /users/{id} — полная замена"""
    email: EmailStr = Field(max_length=255)
    name: str | None = Field(min_length=1, max_length=100)
    phone: str | None = Field(max_length=20)
    address: str | None = Field(max_length=255)
    birth_date: datetime | None = Field(None)


class UserPatch(BaseModel):
    """Тело PATCH /users/{id} — частичное обновление"""
    email: EmailStr | None = Field(None, max_length=255)
    name: str | None = Field(None, min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)
    address: str | None = Field(None, max_length=255)
    birth_date: datetime | None = Field(None)


class UserResponse(BaseModel):
    """Ответ API"""
    id: int
    email: EmailStr
    name: str | None
    created_at: datetime
    phone: str | None
    address: str | None
    birth_date: datetime | None

    class Config:
        from_attributes = True  # pydantic v2
