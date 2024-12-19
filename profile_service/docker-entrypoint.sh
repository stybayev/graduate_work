#!/bin/sh

set -e

# Проверяем окружение и запускаем соответствующий сервер
echo "FASTAPI_ENV: $FASTAPI_ENV"
if [ "$FASTAPI_ENV" = "production" ]; then
    echo "Starting the production server"
    exec gunicorn --worker-class uvicorn.workers.UvicornWorker --config app/core/gunicorn_conf.py app.main:app
else
    echo "Starting the development server"
    exec uvicorn --reload --host=${PROFILE_API_UVICORN_HOST:-0.0.0.0} --port=${PROFILE_API_UVICORN_PORT:-8084} app.main:app
fi
