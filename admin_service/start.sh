#!/bin/bash

set -euo pipefail

# Дождемся, пока база данных будет готова
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for the database at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 0.1
done
echo "Database $POSTGRES_HOST:$POSTGRES_PORT is up and running!"

python manage.py collectstatic --no-input
python manage.py migrate

# Загружаем фикстуру с админом и правами
python manage.py loaddata profiles/fixtures/admin_user
echo "Admin user fixture loaded successfully!"

# Запускаем сервер приложения
echo "Запуск Daphne сервера"

# uvicorn core.asgi:application --host 0.0.0.0 --port 8080 --reload --log-level debug
daphne -b 0.0.0.0 -p 8080 core.asgi:application
