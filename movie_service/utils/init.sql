SELECT 'CREATE DATABASE movie'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'movie')\gexec
CREATE USER movie WITH PASSWORD 'movie';
GRANT ALL PRIVILEGES ON DATABASE "movie" to movie;