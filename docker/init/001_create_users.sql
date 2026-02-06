-- Инициализация БД при первом запуске контейнера postgres (volume docker/init).

-- Таблица users: id (SERIAL), email (NOT NULL UNIQUE), name (nullable), created_at (default now), и другие поля.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT now(),
    phone VARCHAR(20),
    address VARCHAR(255),
    birth_date DATE
);

-- Права для пользователя приложения (POSTGRES_USER из .env).
GRANT USAGE ON SCHEMA public TO api_user;
GRANT SELECT, INSERT, DELETE ON users TO api_user;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO api_user;
