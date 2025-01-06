from functools import lru_cache
from fastapi import Depends, HTTPException, status
from datetime import datetime
from db.mongo import get_db
from utils.enums import ShardedCollections
from schemas.ratings import RatingCreate, RatingsList, RatingUpdate
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import get_current_user


class RatingService:
    def __init__(self, db):
        self.collection = db[ShardedCollections.RATINGS_COLLECTION.collection_name]

    async def create_rating(self,
                            rating: RatingCreate,
                            Authorize: AuthJWT) -> dict:
        """
        Создание рейтинга для фильма
        """
        user_id = await get_current_user(Authorize)

        # Проверяем, не существует ли уже рейтинг от этого пользователя
        existing_rating = await self.collection.find_one({
            "user_id": str(user_id),
            "movie_id": str(rating.movie_id)
        })

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вы уже оценили этот фильм"
            )

        rating_dict = rating.dict()
        rating_dict.update({
            "user_id": str(user_id),
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
            movie_id: str,
            skip: int = 0,
            limit: int = 20
    ) -> RatingsList:
        """
        Получение всех рейтингов фильма
        """
        query = {"movie_id": str(movie_id)}
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
        query = {"user_id": str(user_id)}

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        ratings = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            ratings.append(doc)

        return RatingsList(ratings=ratings, total=total)

    async def update_rating(
            self,
            movie_id: str,
            rating_update: RatingUpdate,
            Authorize: AuthJWT
    ) -> bool:
        """
        Обновление рейтинга фильма
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.update_one(
            {
                "user_id": str(user_id),
                "movie_id": str(movie_id)
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
            movie_id: str,
            Authorize: AuthJWT
    ) -> bool:
        """
        Удаление рейтинга фильма
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.delete_one({
            "user_id": str(user_id),
            "movie_id": str(movie_id)
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рейтинг не найден"
            )

        return True


@lru_cache()
def get_rating_service(db=Depends(get_db)) -> RatingService:
    return RatingService(db)
