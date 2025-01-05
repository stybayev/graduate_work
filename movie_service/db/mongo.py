from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from movie_service.core.config import settings
from movie_service.models.db_models import reviewsCollection


async def init_mongo() -> AsyncIOMotorClient:
    """
    Инициализация Монго
    """
    client = AsyncIOMotorClient(settings.mongo_db.url)
    db = client[settings.mongo_db.default_database]

    await init_beanie(database=db, document_models=[reviewsCollection])
    yield client
    client.close()
