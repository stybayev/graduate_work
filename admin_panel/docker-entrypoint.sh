#!/bin/bash

set -euo pipefail

set -euo pipefail

# Исправляем права доступа при необходимости
if [ ! -x "/opt/app/docker-entrypoint.sh" ]; then
  chmod +x /opt/app/docker-entrypoint.sh
fi

# Ожидаем, пока база данных станет доступной
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for the database at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 0.1
done
echo "Database $POSTGRES_HOST:$POSTGRES_PORT is up and running!"

# Выполняем миграции
echo "Running migrations..."
python manage.py migrate || { echo "Migration failed"; exit 1; }

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --no-input || { echo "Failed to collect static files"; exit 1; }

# Проверка наличия собранных статических файлов
echo "Checking static files..."
ls -l /opt/app/staticfiles || { echo "No static files found"; exit 1; }

# Запуск uWSGI
#echo "Starting uWSGI..."
#uwsgi --strict --ini uwsgi.ini

# Для разработки
python manage.py runserver 0.0.0.0:${DJANGO_PORT}
