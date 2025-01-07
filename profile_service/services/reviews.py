from functools import lru_cache
from fastapi import Depends, HTTPException, status
from datetime import datetime
import httpx

from db.mongo import get_db
from utils.enums import ShardedCollections
from schemas.reviews import (
    ReviewCreate, ReviewsList,
    ReviewUpdate, ReviewPartialUpdate, ReviewResponse
)
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import get_current_user
from core.config import settings
from db.postgres import get_http_client
from uuid import UUID


class ReviewService:
    def __init__(self, db, http_client: httpx.AsyncClient):
        self.collection = db[ShardedCollections.REVIEWS_COLLECTION.collection_name]
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

    async def create_review(self, review: ReviewCreate,
                            Authorize: AuthJWT) -> ReviewResponse:
        """
        Создание рецензии на фильм
        """
        user_id = await get_current_user(Authorize)

        movie_exists = await self.check_movie_exists(review.movie_id)
        if not movie_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фильм не найден"
            )

        # Проверяем, не существует ли уже рецензия от этого пользователя
        existing_review = await self.collection.find_one({
            "user_id": user_id,
            "movie_id": review.movie_id
        })

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вы уже написали рецензию на этот фильм"
            )

        review_dict = review.dict()
        review_dict.update({
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

        result = await self.collection.insert_one(review_dict)
        created_review = await self.collection.find_one({"_id": result.inserted_id})

        if not created_review:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать рецензию"
            )

        created_review["id"] = str(created_review["_id"])
        del created_review["_id"]

        return created_review

    async def get_movie_reviews(
            self,
            movie_id: UUID,
            skip: int = 0,
            limit: int = 20,
            sort_by: str = "created_at",
            sort_order: int = -1
    ) -> ReviewsList:
        """
        Получение всех рецензий фильма с сортировкой
        """
        query = {"movie_id": movie_id}
        total = await self.collection.count_documents(query)

        cursor = self.collection.find(query) \
            .sort(sort_by, sort_order) \
            .skip(skip) \
            .limit(limit)

        reviews = []
        async for doc in cursor:
            try:
                review_data = {
                    "id": str(doc["_id"]),
                    "movie_id": doc["movie_id"],
                    "user_id": doc["user_id"],
                    "text": doc.get("text", ""),
                    "title": doc.get("title", ""),
                    "created_at": doc.get("created_at", datetime.utcnow()),
                    "updated_at": doc.get("updated_at")
                }
                reviews.append(review_data)
            except Exception as e:
                logging.info(f"Error processing review: {e}")
                continue

        return ReviewsList(reviews=reviews, total=total)

    async def get_user_reviews(
            self,
            Authorize: AuthJWT,
            skip: int = 0,
            limit: int = 20
    ) -> ReviewsList:
        """
        Получение всех рецензий пользователя
        """
        user_id = await get_current_user(Authorize)
        query = {"user_id": user_id}

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        reviews = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            reviews.append(doc)

        return ReviewsList(reviews=reviews, total=total)

    async def update_review(
            self,
            movie_id: UUID,
            review_update: ReviewUpdate,
            Authorize: AuthJWT
    ) -> bool:
        """
        Обновление рецензии на фильм
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.update_one(
            {
                "user_id": user_id,
                "movie_id": movie_id
            },
            {
                "$set": {
                    **review_update.dict(),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рецензия не найдена"
            )

        return True

    async def patch_review(
            self,
            movie_id: UUID,
            review_update: ReviewPartialUpdate,
            Authorize: AuthJWT
    ) -> bool:
        """
        Частичное обновление рецензии
        """
        user_id = await get_current_user(Authorize)

        update_data = review_update.dict(exclude_unset=True)
        if not update_data:
            return True

        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {
                "user_id": user_id,
                "movie_id": movie_id
            },
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рецензия не найдена"
            )

        return True

    async def delete_review(
            self,
            movie_id: UUID,
            Authorize: AuthJWT
    ) -> bool:
        """
        Удаление рецензии на фильм
        """
        user_id = await get_current_user(Authorize)

        result = await self.collection.delete_one({
            "user_id": user_id,
            "movie_id": movie_id
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рецензия не найдена"
            )

        return True


@lru_cache()
def get_review_service(
        db=Depends(get_db),
        http_client: httpx.AsyncClient = Depends(get_http_client)
) -> ReviewService:
    return ReviewService(db, http_client)
