import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from movie_service.core.logger import LOGGING


class DataBaseSettings(BaseSettings):
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_file = ".env"
        env_prefix = "MOVIE_"

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class MongoDataBaseSettings(BaseSettings):
    initdb_root_username: str = ...
    initdb_root_password: str = ...
    default_database: str = ...
    host: str = ...
    port: int = ...
    collection: str = ...

    class Config:
        env_file = ".env"
        env_prefix = "MONGO_"

    @property
    def url(self):
        return f"mongodb://{self.initdb_root_username}:{self.initdb_root_password}@{self.host}:{self.port}"


class Settings(BaseSettings):
    # App
    project_name: str = Field(default="Movie API", env="Movie API")
    description: str = Field(default="A service for getting information about movies")
    uvicorn_host: str = Field(default="0.0.0.0", env="MOVIE_API_UVICORN_HOST")
    uvicorn_port: int = Field(default=8085, env="MOVIE_API_UVICORN_PORT")
    # Postgres
    db: DataBaseSettings = DataBaseSettings()
    log_sql_queries: bool = False
    # Mongo
    mongo_db = MongoDataBaseSettings()


# Создаем экземпляр класса Settings для хранения настроек
settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
