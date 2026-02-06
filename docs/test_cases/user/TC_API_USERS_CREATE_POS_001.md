# Test Case: Create User (POST /users)

| Поле | Описание |
|------|----------|
| **Test Case ID** | TC_API_USERS_CREATE_POS_001 |
| **Название** | Успешное создание пользователя |
| **Цель теста** | Проверить, что API успешно создаёт пользователя при валидных данных и возвращает корректный ответ |
| **Тип теста** | API / Integration |
| **Категория** | Positive |
| **Приоритет** | High |
| **Теги** | users, create, smoke, regression |
| **Automation Ready** | Да |
| **Предусловия** | API и PostgreSQL запущены (Docker); пользователь с таким email отсутствует в БД |
| **HTTP Метод** | POST |
| **Endpoint** | `/users` |
| **Headers** | `Content-Type: application/json` |
| **Query Params** | — |
| **Body (Payload)** | `{ "email": "test_<uuid>@example.com", "name": "John Doe" }` |
| **Источник тестовых данных** | Генерация данных в тесте (UUID) |
| **Ожидаемый HTTP статус** | `201 Created` |
| **Ожидаемый Response (Schema)** | `id: number`, `email: string`, `name: string | null`, `created_at: datetime` |
| **Assertions** | `status == 201`; `id` присутствует; `email == payload.email`; `name == payload.name`; `created_at` не пустой |
| **DB Checks (опционально)** | В таблице `users` существует запись с возвращённым `id` и `email` |
| **Постусловия** | Пользователь удалён из БД (cleanup через прямое подключение) |
| **Зависимости** | — |
