#!/bin/sh

set -e

# Если передана команда мигарции alembic, выполнить её напрямую
if [ "$1" = "alembic" ]; then
    exec "$@"
fi

# Иначе запускаем сервер как обычно
echo "FASTAPI_ENV: $FASTAPI_ENV"
if [ "$FASTAPI_ENV" = "production" ]; then
    echo "Starting the production server"
    exec gunicorn --worker-class uvicorn.workers.UvicornWorker --config core/gunicorn_conf.py profile_service.main:app
else
    echo "Starting the development server"
    exec uvicorn --reload --host=${PROFILE_API_UVICORN_HOST:-0.0.0.0} --port=${PROFILE_API_UVICORN_PORT:-8084} main:app
fi