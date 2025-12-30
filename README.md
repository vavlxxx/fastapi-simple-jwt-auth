### Шаблон для простого FastAPI приложения с JWT авторизацией

Данное приложение имеет пять основных ручек, связанных с авторизацией пользователя:

 - POST /api/v1/register - регистрация пользователя
 - POST /api/v1/login - вход в акканут
 - GET /api/v1/profile - профиль пользователя
 - PUT /api/v1/profile - обновить профиль
 - POST /api/v1/refresh - получить новые Refresh и Access токены
 - POST /api/v1/logout - Выход из аккаунта 

#### Генерирование ключей для JWT токенов

Для подписи JWT токенов используются ключи, которые хранятся в директории `creds/` (её нужно создать). Далее необходимо перейти в неё и воспользоваться командами ниже, чтобы создать приватный и публичный ключ.

```bash
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

#### Настройка переменных окружения

По примеру из шаблонного файла `.env.template` необходимо создать файлы с переменными окружения:

 - `.env`: основной файл для локального запуска;
 - `.env.docker`: повторяет `.env`, но сконфигурирован для Docker сети; 
 - `.env.test`: повторяет `.env`, но хранит данные для тестирования;
 - `.env.postgres`: параметры PostgreSQL для docker контейнера.

Ниже представлена настройка для основного `.env` файла с уточнениями для других.

```bash
### .env (.env.test, .env.docker)

# database config

CFG_DB__DB_HOST=localhost # в .env.docker будет название контейнера с PostgreSQL
CFG_DB__DB_USER=postgres
CFG_DB__DB_NAME=postgres # в .env.test будет название тестовой БД (должно совпасть с DB_NAME_TEST)
CFG_DB__DB_PORT=5432 # для .env.docker будет прокинутый порт
CFG_DB__DB_PASSWORD=postgres

# app config

# использует PostgreSQL для DEV и для TEST
CFG_APP__MODE=DEV # TEST для .env.test - определяет DSN

### .env.postgres

# переменные для контейнера PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

Для проведения миграций при помощи Alembic необходимо:
 - для тестовой БД `CFG_APP__MODE` установить в `TEST`;
 - для PostgreSQL `CFG_APP__MODE` установить  в `DEV`.


```bash
poetry run alembic revision --autogenerate -m "basic: created basic tables for example"
```

#### Запуск

Для запуска достаточно собрать все контейнеры при помощи Docker Compose. При необходимости синхронизации контейнера FastAPI приложения каждый раз при сохранении изменений в проекте можно передать флаг `--watch`.

```bash
docker compose up --build --watch
```

#### Тестирование

Для проверки работоспособности были написаны базовые тесты, покрывающие базовые CRUD операции. Для запуска необходимо активировать виртуальное окружение (или воспользоваться `poetry run ...`) и ввести:

```
pytest -s -v
```
