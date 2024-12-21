"""
Конфигурация приложения.

Этот модуль содержит классы и настройки для управления конфигурацией приложения.
"""

import os

from pydantic.v1 import BaseSettings


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

    # App
    project_name: str
    uvicorn_host: str
    uvicorn_port: int

    # Postgres
    db: DataBaseSettings = DataBaseSettings()
    log_sql_queries: bool = False

    class Config:
        """Конфигурация для загрузки переменных окружения."""

        env_file = '.env'
        env_prefix = 'PROFILE_API_'


# Создаем экземпляр класса Settings для хранения настроек
settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # noqa: WPS221
