-- Создание БД и пользователя
CREATE USER profile_service WITH PASSWORD 'profile_service';
CREATE DATABASE profile_service;
GRANT ALL PRIVILEGES ON DATABASE profile_service TO profile_service;

-- Подключение к созданной БД
\c profile_service;

-- Создание схемы и выдача прав
CREATE SCHEMA IF NOT EXISTS profiles_service;
GRANT ALL ON SCHEMA profiles_service TO profile_service;
GRANT ALL ON ALL TABLES IN SCHEMA profiles_service TO profile_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA profiles_service GRANT ALL ON TABLES TO profile_service;