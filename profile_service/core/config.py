"""
Конфигурация приложения.

Этот модуль содержит классы и настройки для управления конфигурацией приложения.
"""

import os

from pydantic.v1 import BaseSettings


class JWTSettings(BaseSettings):
    """
    Настройки JWT
    """
    authjwt_secret_key: str = ...
    authjwt_algorithm: str = ...
    authjwt_access_token_expires: int = ...
    authjwt_refresh_token_expires: int = ...
    authjwt_user_claims: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "PROFILE_API_"


class DataBaseSettings(BaseSettings):
    """
    Настройки подключения к базе данных PostgreSQL.

    Атрибуты:
        user: Имя пользователя для подключения.
        password: Пароль пользователя.
        db: Имя базы данных.
        host: Хост базы данных.
        port: Порт базы данных.
    """

    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    class Config:
        """Конфигурация для загрузки переменных окружения."""

        env_file = '.env'
        env_prefix = 'DB_PROFILE_SERVICE_'

    @property
    def url(self) -> str:
        """
        Генерация URL для подключения к базе данных.

        Returns:
            str: URL для подключения.
        """
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'  # noqa: WPS221, WPS305, E501


class MovieServiceSettings(BaseSettings):
    """
    Настройки сервиса фильмов
    """
    host: str = 'movie_service'
    port: int = 8085

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1/movie"


class MongoDataBaseSettings(BaseSettings):
    initdb_root_username: str = ...
    initdb_root_password: str = ...
    default_database: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_file = ".env"
        env_prefix = "MONGO_"

    @property
    def url(self):
        return f"mongodb://{self.initdb_root_username}:{self.initdb_root_password}@{self.host}:{self.port}"


class Settings(BaseSettings):
    """
    Основные настройки приложения.

    Атрибуты:
        project_name: Название проекта.
        uvicorn_host: Хост для Uvicorn.
        uvicorn_port: Порт для Uvicorn.
        db: Настройки базы данных.
        log_sql_queries: Флаг для логирования SQL-запросов.
    """
    # JWT
    jwt: JWTSettings = JWTSettings()

    # App
    project_name: str
    uvicorn_host: str
    uvicorn_port: int

    # Postgres
    db: DataBaseSettings = DataBaseSettings()
    log_sql_queries: bool = False

    # MongoDB
    mongo_db: MongoDataBaseSettings = MongoDataBaseSettings()

    # Movie API
    movie_service = MovieServiceSettings()

    class Config:
        """Конфигурация для загрузки переменных окружения."""

        env_file = '.env'
        env_prefix = 'PROFILE_API_'


# Создаем экземпляр класса Settings для хранения настроек
settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: WPS221
