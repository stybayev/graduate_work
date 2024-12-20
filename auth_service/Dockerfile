FROM --platform=linux/amd64 python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /auth_service
COPY requirements.txt /auth_service
RUN /usr/local/bin/python -m pip install --upgrade pip \
&& apt-get update -y \
&& apt-get install gcc -y \
&& pip install -r requirements.txt
COPY . /auth_service

CMD uvicorn --reload --host=$AUTH_API_UVICORN_HOST --port=$AUTH_API_UVICORN_PORT main:app
