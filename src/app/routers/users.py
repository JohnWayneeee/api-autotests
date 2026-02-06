"""
Роутер /users.

CRUD для пользователей:
- GET    /users/{id}      — получить пользователя
- POST   /users           — создать пользователя
- PUT    /users/{id}      — полное обновление
- PATCH  /users/{id}      — частичное обновление
- DELETE /users/{id}      — удалить пользователя

Реализация СИНХРОННАЯ, т.к. используется psycopg2.
"""

from fastapi import APIRouter, HTTPException, status

from ..deps import get_db_connection, get_db_cursor
from ..schemas import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    GET /users/{user_id}

    Возвращает пользователя по id.
    Если не найден — 404.
    """
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            cur.execute(
                """
                SELECT id, email, name, created_at, phone, address, birth_date
                FROM users
                WHERE id = %s;
                """,
                (user_id,),
            )
            row = cur.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return row


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(payload: UserCreate):
    """
    POST /users

    Создаёт нового пользователя.
    Email должен быть уникальным.
    """
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO users (email, name, phone, address, birth_date)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, email, name, created_at, phone, address, birth_date;
                    """,
                    (payload.email, payload.name, payload.phone, payload.address,
                     payload.birth_date),
                )
                row = cur.fetchone()
            except Exception:
                # Обычно здесь ловят UniqueViolation,
                # но тип исключения зависит от настроек psycopg2
                raise HTTPException(
                    status_code=409,
                    detail="User with this email already exists",
                )
        
        conn.commit()
    
    return row


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate):
    """
    PUT /users/{user_id}

    Полное обновление пользователя.
    Все поля обязательны.
    """
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            cur.execute(
                """
                UPDATE users
                SET email = %s,
                    name = %s,
                    phone = %s,
                    address = %s,
                    birth_date = %s
                WHERE id = %s
                RETURNING id, email, name, created_at, phone, address, birth_date;
                """,
                (payload.email, payload.name, payload.phone, payload.address,
                 payload.birth_date,
                 user_id),
            )
            row = cur.fetchone()
        
        conn.commit()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return row


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, payload: UserPatch):
    """
    PATCH / users/{user_id}

    Частичное обновление пользователя.
    Можно передать любое подмножество полей.
    """
    data = payload.model_dump(exclude_unset=True)
    
    if not data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update",
        )
    
    fields = ", ".join(f"{key} = %s" for key in data.keys())
    values = list(data.values()) + [user_id]
    
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            cur.execute(
                f"""
                UPDATE users
                SET {fields}
                WHERE id = %s
                RETURNING id, email, name, created_at, phone, address, birth_date;
                """,
                values,
            )
            row = cur.fetchone()
        
        conn.commit()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return row


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """
    DELETE / users/{user_id}

    Удаляет пользователя.
    Возвращает 204 при успехе.
    """
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s RETURNING id;",
                (user_id,),
            )
            deleted = cur.fetchone()
        
        conn.commit()
    
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
