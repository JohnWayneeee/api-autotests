"""
Точка входа FastAPI: приложение и подключение роутеров.
Запуск: uvicorn src.app.main:app --host 127.0.0.1 --port 8000
"""

from fastapi import FastAPI

from .routers import users


app = FastAPI(
    title="API Autotests",
    version="0.1.0",
    description="""
Пет-проект **Senior AQA Python**.

REST API на **FastAPI** с полным CRUD по пользователям
и автотестами на **pytest / requests / pydantic**.

### Возможности
- CRUD `/users` с расширенными полями (phone, address, birth_date)
- Валидация запросов и ответов через Pydantic
- PostgreSQL + psycopg2
- Готово для unit и e2e тестирования

Проект используется для практики API-тестирования и CI.
""",
)
# Все эндпоинты /users — в роутере users
app.include_router(users.router)
