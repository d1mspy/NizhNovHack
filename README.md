Запуск желателен на Linux-системах, требуется установленный Docker

шаблон .env
```
APP_PG__USER={username}
APP_PG__HOST=postgres
APP_PG__PORT=5432
APP_PG__PASSWORD={password}
APP_PG__DATABASE={database}

APP_AI__API_KEY={API_KEY}
```
Поля в круглых скобках необходимо задать свои, хост и порт оставить как здесь

Запуск
```
docker compose build
docker compose up
```
