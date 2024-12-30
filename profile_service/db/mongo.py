from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from enum import Enum

from profile_service.core.config import settings

client = AsyncIOMotorClient(settings.db.url)
mongo_db = client[settings.mongo_db.default_database]


async def shard_collections(collections: Enum):
    """
    Функция шардирования и создания коллекций.
    """
    await client.admin.command("enableSharding", settings.mongo_db.default_database)

    mongo_db = client[settings.mongo_db.default_database]

    for collection in collections:
        collection_names = await mongo_db.list_collection_names()
        if collection.collection_name not in collection_names:
            await mongo_db.create_collection(collection.collection_name)

        shard_key = collection.shard_key
        await client.admin.command(
            "shardCollection",
            f"{settings.mongo_db.default_database}.{collection.collection_name}",
            key=shard_key
        )


async def get_db() -> AsyncGenerator:
    try:
        yield mongo_db
    finally:
        pass