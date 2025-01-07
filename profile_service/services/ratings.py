from functools import lru_cache
from fastapi import Depends, HTTPException, status
from datetime import datetime
from db.mongo import get_db
from utils.enums import ShardedCollections
from schemas.ratings import (
    RatingCreate, RatingsList,
    RatingUpdate, MovieAverageRating)
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import get_current_user
import httpx
from core.config import settings

from db.postgres import get_http_client
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID


class RatingService:
    def __init__(self, db, http_client: httpx.AsyncClient):
        self.collection = db[ShardedCollections.RATINGS_COLLECTION.collection_name]
        self.http_client = http_client

    async def check_movie_exists(self, movie_id: UUID) -> bool:
        """
        Проверка существования фильма
        """
        try:
            response = await self.http_client.get(
                f"{settings.movie_service.url}/get_film",
                params={"film_id": movie_id}
            )
            return response.status_code == status.HTTP_200_OK
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис фильмов недоступен"
            )

    async def create_rating(self,
                            rating: RatingCreate,
                            Authorize: AuthJWT) -> dict:
        """
        Создание рейтинга для фильма
        """
        user_id = await get_current_user(Authorize)

        movie_exists = await self.check_movie_exists(rating.movie_id)
        if not movie_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фильм не найден"
            )

        # Проверяем, не существует ли уже рейтинг от этого пользователя
        existing_rating = await self.collection.find_one({
            "user_id": user_id,
            "movie_id": rating.movie_id
        })

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вы уже оценили этот фильм"
            )

        rating_dict = rating.dict()
        rating_dict.update({
            "user_id": user_id,
            "created_at": datetime.utcnow()
        })

        result = await self.collection.insert_one(rating_dict)
        created_rating = await self.collection.find_one({"_id": result.inserted_id})

        if not created_rating:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать рейтинг"
            )

        return created_rating

    async def get_movie_ratings(
            self,
            movie_id: UUID,
            skip: int = 0,
            limit: int = 20
    ) -> RatingsList:
        """
        Получение всех рейтингов фильма
        """
        query = {"movie_id": movie_id}
        total = await self.collection.count_documents(query)

        cursor = self.collection.find(query).skip(skip).limit(limit)
        ratings = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            ratings.append(doc)

        return RatingsList(ratings=ratings, total=total)

    async def get_user_ratings(
            self,
            Authorize: AuthJWT,
            skip: int = 0,
            limit: int = 20
    ) -> RatingsList:
        """
        Получение всех рейтингов пользователя
        """
        user_id = await get_current_user(Authorize)
        query = {"user_id": user_id}

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        ratings = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            ratings.append(doc)

        return RatingsList(ratings=ratings, total=total)

    async def update_rating(
            self,
            movie_id: UUID,
            rating_update: RatingUpdate,
            Authorize: AuthJWT
    ) -> bool:
        """
        Обновление рейтинга фильма
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.update_one(
            {
                "user_id": user_id,
                "movie_id": movie_id
            },
            {"$set": {
                "rating": rating_update.rating,
                "updated_at": datetime.utcnow()
            }}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рейтинг не найден"
            )

        return True

    async def delete_rating(
            self,
            movie_id: UUID,
            Authorize: AuthJWT
    ) -> bool:
        """
        Удаление рейтинга фильма
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.delete_one({
            "user_id": user_id,
            "movie_id": movie_id
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рейтинг не найден"
            )

        return True

    async def get_movie_average_rating(self, movie_id: UUID) -> MovieAverageRating:
        """
        Получение среднего рейтинга фильма
        """
        pipeline = [
            {"$match": {"movie_id": movie_id}},
            {
                "$group": {
                    "_id": "$movie_id",
                    "average_rating": {"$avg": "$rating"},
                    "total_ratings": {"$sum": 1}
                }
            }
        ]

        result = await self.collection.aggregate(pipeline).to_list(length=1)

        if not result:
            return MovieAverageRating(
                movie_id=movie_id,
                average_rating=0.0,
                total_ratings=0
            )

        return MovieAverageRating(
            movie_id=movie_id,
            average_rating=round(result[0]["average_rating"], 2),
            total_ratings=result[0]["total_ratings"]
        )


@lru_cache()
def get_rating_service(db: AsyncIOMotorClient = Depends(get_db),
                       http_client: httpx.AsyncClient = Depends(get_http_client)) -> RatingService:
    return RatingService(db, http_client)
