# Podcast Platform API

**Backend** для полноценной платформы управления подкастами, авторами и их слушателей. Решение включает в себя аналитику, монетизацию и JWT-аутентификацию.

Проект демонстрирует навыки архитектуры REST API, работы с реляционными БД и реализации бизнес-логики на Python.

---

## Ключевой функционал

- **Управление пользователями**: Регистрация слушателей и авторов, рейтинг авторов.
- **Контент**: Создание подкастов и выпусков, комментирование.
- **Монетизация**: Freemium-подписки (бесплатные/премиум уровни), учет платежей.
- **Аналитика**: Отчеты по популярности контента, доходам платформы и истории прослушиваний.
- **Безопасность**: JWT-аутентификация, хеширование паролей (bcrypt), разделение ролей (listener/author/admin).
- **Пагинация**: Все `GET` списковые эндпоинты поддерживают пагинацию.
- **Контейнеризация**: Docker Compose

---

## Технологический стек

- Python 3.14
- Docker
- FastAPI
- PostgreSQL
- psycopg2
- Pydantic
- Swagger UI
- JWT (JSON Web Tokens)
- bcrypt
  

---

## Быстрый старт(Docker и без)

### 1. Требования
- Python 3.14 или выше
- PostgreSQL 18 или выше
- pip
- docker.desktop

### 2. Клонирование репозитория

```bash
git clone https://github.com/yourusername/podcast-platform.git
cd podcast-platform
```

### Запуск через Docker

```bash
docker-compose up -d
```

### 3. Настройка виртуального окружения (Далее без docker)

```bash
python -m venv venv

# Windows
venvScriptsactivate

# Linux / macOS
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка базы данных

Создайте базу данных в PostgreSQL:

```bash
psql -U postgres -c "CREATE DATABASE podcast;"
```

Выполните SQL скрипты из директории sql/:

```bash
psql -U postgres -d podcast -f sql/01_schema.sql
psql -U postgres -d podcast -f sql/02_seed_data.sql
psql -U postgres -d podcast -f sql/03_views.sql
psql -U postgres -d podcast -f sql/04_users.sql
```

### 6. Конфигурация

Создайте файл .env в корне проекта:

```bash
DB_NAME=podcast
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-super-secret-key
API_PORT=8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 7. Запуск сервера

```bash
python main.py
```

Сервер будет доступен по адресу http://localhost:8000

Документация API: http://localhost:8000/docs

### 8. Запуск через Docker

```bash
docker-compose up -d
```

---

## Аутентификация

API использует JWT токены для защиты эндпоинтов.

### Регистрация

```bash
curl -X POST http://localhost:8000/auth/register 
-H "Content-Type: application/json" 
-d '{
"email": "user@example.com",
"password": "secure_password",
"role": "listener"
}'
```

Роли: listener, author, admin.

### Вход в систему

```bash
curl -X POST http://localhost:8000/auth/login 
-H "Content-Type: application/x-www-form-urlencoded" 
-d "username=user@example.com&password=secure_password"
```

Ответ содержит access_token, который используется для доступа к защищенным эндпоинтам.

---

## Структура базы данных

### Таблицы

| Таблица       | Назначение                           |
|---------------|--------------------------------------|
| Users         | Пользователи системы (аутентификация)|
| Listeners     | Слушатели платформы                  |
| Authors       | Авторы подкастов                     |
| Podcasts      | Подкасты                             |
| Episodes      | Эпизоды подкастов                    |
| Subscriptions | Подписки слушателей на авторов       |
| Payments      | Платежи за премиум подписки          |
| Comments      | Комментарии к эпизодам               |
| Listening     | История прослушиваний                |

### Представления

| Представление       | Назначение                   |
|---------------------|------------------------------|
| podcast_stats       | Статистика по подкастам      |
| author_analytics    | Аналитика по авторам         |
| listener_activity   | Активность слушателей        |

---

## API Endpoints

### Аутентификация

| Метод | Путь           | Описание                      |
|-------|----------------|-------------------------------|
| POST  | /auth/register | Регистрация пользователя      |
| POST  | /auth/login    | Вход и получение токена       |
| GET   | /auth/me       | Информация о текущем пользователе |

### Слушатели

| Метод | Путь                              | Описание                     | Доступ     |
|-------|-----------------------------------|------------------------------|------------|
| GET   | /listeners/                       | Получить всех слушателей     | Публичный  |
| GET   | /listeners/{id}                   | Получить слушателя по ID     | Публичный  |
| POST  | /listeners/                       | Создать слушателя            | Пользователь|
| PUT   | /listeners/{id}                   | Обновить статус подписки     | Пользователь|
| GET   | /listeners/{id}/subscriptions     | Подписки слушателя           | Публичный  |
| GET   | /listeners/{id}/history           | История прослушиваний        | Публичный  |
| DELETE| /listeners/{id}                   | Удалить слушателя            | Админ      |

### Авторы

| Метод | Путь                          | Описание                   | Доступ     |
|-------|-------------------------------|----------------------------|------------|
| GET   | /authors/                     | Получить всех авторов      | Публичный  |
| GET   | /authors/{id}                 | Получить автора по ID      | Публичный  |
| POST  | /authors/                     | Создать автора             | Пользователь|
| PUT   | /authors/{id}/rating          | Обновить рейтинг автора    | Пользователь|
| GET   | /authors/{id}/podcasts        | Подкасты автора            | Публичный  |
| GET   | /authors/{id}/subscribers     | Подписчики автора          | Публичный  |
| DELETE| /authors/{id}                 | Удалить автора             | Админ      |

### Подкасты

| Метод | Путь                       | Описание                   | Доступ     |
|-------|----------------------------|----------------------------|------------|
| GET   | /podcasts/                 | Получить все подкасты      | Публичный  |
| GET   | /podcasts/search/          | Поиск подкастов            | Публичный  |
| GET   | /podcasts/{id}             | Получить подкаст по ID     | Публичный  |
| POST  | /podcasts/                 | Создать подкаст            | Пользователь|
| GET   | /podcasts/{id}/episodes    | Эпизоды подкаста           | Публичный  |
| DELETE| /podcasts/{id}             | Удалить подкаст            | Админ      |

### Эпизоды

| Метод | Путь                           | Описание                       | Доступ     |
|-------|--------------------------------|--------------------------------|------------|
| GET   | /episodes/                     | Получить все эпизоды           | Публичный  |
| GET   | /episodes/{id}                 | Получить эпизод по ID          | Публичный  |
| POST  | /episodes/                     | Создать эпизод                 | Пользователь|
| POST  | /episodes/listen/              | Записать прослушивание         | Публичный  |
| GET   | /episodes/{id}/comments        | Комментарии к эпизоду          | Публичный  |
| POST  | /episodes/{id}/comments        | Добавить комментарий           | Пользователь|

### Подписки

| Метод | Путь                 | Описание                       | Доступ     |
|-------|----------------------|--------------------------------|------------|
| GET   | /subscriptions/      | Получить все подписки          | Публичный  |
| POST  | /subscriptions/      | Создать подписку               | Пользователь|
| DELETE| /subscriptions/{id}  | Отменить подписку              | Пользователь|

### Платежи

| Метод | Путь            | Описание                   | Доступ     |
|-------|-----------------|----------------------------|------------|
| GET   | /payments/      | Получить все платежи       | Админ      |
| POST  | /payments/      | Создать платеж             | Пользователь|

### Аналитика

| Метод | Путь                       | Описание                       | Доступ     |
|-------|----------------------------|--------------------------------|------------|
| GET   | /analytics/popular/        | Популярные подкасты            | Публичный  |
| GET   | /analytics/top-authors/    | Топ авторов по подписчикам     | Публичный  |
| GET   | /analytics/revenue/        | Общая выручка                  | Админ      |
| GET   | /analytics/stats/          | Общая статистика платформы     | Публичный  |

---

## Примеры запросов

### Создание слушателя

```bash
curl -X POST http://localhost:8000/listeners/ 
-H "Content-Type: application/json" 
-H "Authorization: Bearer <token>" 
-d '{
"name": "Иван Петров",
"email": "ivan@mail.ru",
"sub_status": "Премиум"
}'
```

### Создание подкаста

```bash
curl -X POST http://localhost:8000/podcasts/ 
-H "Content-Type: application/json" 
-H "Authorization: Bearer <token>" 
-d '{
"title": "Python для начинающих",
"description": "Изучаем Python с нуля",
"id_author": 1
}'
```

### Получение слушателей с пагинацией

```bash
curl -X GET "http://localhost:8000/listeners/?page=1&size=10"
```

### Запись прослушивания

```bash
curl -X POST http://localhost:8000/episodes/listen/ 
-H "Content-Type: application/json" 
-d '{
"id_listener": 1,
"id_episode": 1,
"duration_listened": 45
}'
```

---

## Структура проекта

```
podcast-platform/
├── main.py
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── sql/
│   ├── 01_schema.sql
│   ├── 02_seed_data.sql
│   ├── 03_views.sql
│   └── 04_users.sql
└── src/
    ├── __init__.py
    ├── config.py
    ├── auth.py
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py
    │   └── models.py
    ├── services/
    │   ├── __init__.py
    │   ├── listener_service.py
    │   ├── author_service.py
    │   ├── podcast_service.py
    │   ├── episode_service.py
    │   ├── subscription_service.py
    │   ├── payment_service.py
    │   ├── analytics_service.py
    │   └── report_service.py
    ├── api/
    │   ├── __init__.py
    │   ├── routes.py
    │   └── auth_routes.py
    └── utils/
        ├── __init__.py
        ├── exceptions.py
        └── validators.py
```

---
