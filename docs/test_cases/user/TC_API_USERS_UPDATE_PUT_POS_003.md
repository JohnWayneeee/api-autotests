# Test Case: Update User (PUT /users/{id})

| Поле                            | Описание                                                                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------- | ------------------------ | ----- |
| **Test Case ID**                | TC_API_USERS_UPDATE_PUT_POS_003                                                                                                                      |
| **Название**                    | Успешное полное обновление пользователя                                                                                                              |
| **Цель теста**                  | Проверить, что API успешно обновляет все данные пользователя методом PUT при валидных данных                                                         |
| **Тип теста**                   | API / Integration                                                                                                                                    |
| **Категория**                   | Positive                                                                                                                                             |
| **Приоритет**                   | High                                                                                                                                                 |
| **Теги**                        | users, update, put, positive, regression                                                                                                             |
| **Automation Ready**            | Да                                                                                                                                                   |
| **Предусловия**                 | API и PostgreSQL запущены (Docker); существует пользователь с известным ID в БД                                                                      |
| **HTTP Метод**                  | PUT                                                                                                                                                  |
| **Endpoint**                    | `/users/{id}`                                                                                                                                        |
| **Headers**                     | `Content-Type: application/json`                                                                                                                     |
| **Query Params**                | —                                                                                                                                                    |
| **Path Variables**              | `id: number` (валидный ID существующего пользователя)                                                                                                |
| **Body (Payload)**              | `{ "email": "updated_test@example.com", "name": "Updated Name", "phone": "+79991234567", "address": "Updated Address", "birth_date": "1990-01-01" }` |
| **Источник тестовых данных**    | Генерация обновленных данных в тесте                                                                                                                 |
| **Ожидаемый HTTP статус**       | `200 OK`                                                                                                                                             |
| **Ожидаемый Response (Schema)** | `id: number`, `email: string`, `name: string                                                                                                         | null`, `created_at: datetime`, `phone: string | null`, `address: string | null`, `birth_date: date | null` |
| **Assertions**                  | `status == 200`; `id` соответствует запрошенному; все поля обновлены в соответствии с payload; `created_at` не изменен                               |
| **DB Checks (опционально)**     | В таблице `users` запись с указанным `id` содержит обновленные данные                                                                                |
| **Постусловия**                 | Пользователь восстановлен до начального состояния (cleanup)                                                                                          |
| **Зависимости**                 | —                                                                                                                                                    |
