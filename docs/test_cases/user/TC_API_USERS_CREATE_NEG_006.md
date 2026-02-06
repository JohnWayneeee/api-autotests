# Test Case: Create User with Duplicate Email (POST /users)

| Поле                            | Описание                                                                                                                    |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**                | TC_API_USERS_CREATE_NEG_006                                                                                                 |
| **Название**                    | Ошибка при создании пользователя с дублирующимся email                                                                      |
| **Цель теста**                  | Проверить, что API возвращает корректную ошибку при попытке создания пользователя с email, который уже существует в системе |
| **Тип теста**                   | API / Integration                                                                                                           |
| **Категория**                   | Negative                                                                                                                    |
| **Приоритет**                   | High                                                                                                                        |
| **Теги**                        | users, create, negative, validation, regression                                                                             |
| **Automation Ready**            | Да                                                                                                                          |
| **Предусловия**                 | API и PostgreSQL запущены (Docker); существует пользователь с известным email в БД                                          |
| **HTTP Метод**                  | POST                                                                                                                        |
| **Endpoint**                    | `/users`                                                                                                                    |
| **Headers**                     | `Content-Type: application/json`                                                                                            |
| **Query Params**                | —                                                                                                                           |
| **Body (Payload)**              | `{ "email": "existing_user@example.com", "name": "Another John Doe" }` (email совпадает с существующим)                     |
| **Источник тестовых данных**    | Email существующего пользователя из БД                                                                                      |
| **Ожидаемый HTTP статус**       | `409 Conflict`                                                                                                              |
| **Ожидаемый Response (Schema)** | `{ "detail": string }`                                                                                                      |
| **Assertions**                  | `status == 409`; тело ответа содержит информацию об ошибке; пользователь не создан в БД                                     |
| **DB Checks (обязательно)**     | В таблице `users` отсутствует дубликат пользователя с тем же email                                                          |
| **Постусловия**                 | —                                                                                                                           |
| **Зависимости**                 | —                                                                                                                           |
