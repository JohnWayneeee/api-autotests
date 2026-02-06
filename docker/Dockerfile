# =====================================================
# ИНСТРУКЦИЯ ПО ЗАПУСКУ
# =====================================================
# 1. КОПИРУЙТЕ .env в docker/.env (POSTGRES_USER=api_user, POSTGRES_PASSWORD=api_pass)
# 2. Из КОРНЯ ПРОЕКТА (api-autotests):
#    docker compose -f docker/docker-compose.yaml up -d --build
# 3. API: http://localhost:3000/docs
#    БД: localhost:5432 (CloudBeaver: localhost:8978)
# 4. ТЕСТЫ: docker compose -f docker/docker-compose.yaml --profile test up
# 5. ОСТАНОВКА: docker compose -f docker/docker-compose.yaml down -v
# =====================================================

FROM python:3.12-slim

WORKDIR /app

# Установка uv (быстрый pip alternative) + зависимости (без dev)
COPY pyproject.toml uv.lock* ./
RUN pip install uv && \
    uv sync --no-dev --no-install-project && \
    rm -rf /root/.cache/pip

# Код приложения
COPY src ./src

# Переменные окружения
ENV PYTHONPATH=/app \
    UV_NO_CACHE=1

EXPOSE 3000

# По умолчанию: FastAPI dev сервер
CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
