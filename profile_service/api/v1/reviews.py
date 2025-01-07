from fastapi import APIRouter, Depends, Query
from typing import Annotated
from services.reviews import ReviewService, get_review_service
from schemas.reviews import (
    ReviewCreate, ReviewUpdate,
    ReviewsList, ReviewPartialUpdate, ReviewResponse
)
from async_fastapi_jwt_auth import AuthJWT
from uuid import UUID

from dependencies.auth import security_jwt

router = APIRouter()


@router.post("/", response_model=ReviewResponse)
async def create_review(
        review: ReviewCreate,
        review_service: ReviewService = Depends(get_review_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Создание новой рецензии на фильм
    """
    return await review_service.create_review(review, Authorize)


@router.get("/movie/{movie_id}", response_model=ReviewsList)
async def get_movie_reviews(
        movie_id: UUID,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        sort_by: str = "created_at",
        sort_order: int = -1,
        review_service: ReviewService = Depends(get_review_service),
):
    """
    Получение всех рецензий для конкретного фильма
    """
    return await review_service.get_movie_reviews(
        movie_id, skip, limit, sort_by, sort_order
    )


@router.get("/user", response_model=ReviewsList)
async def get_user_reviews(
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,

        review_service: ReviewService = Depends(get_review_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Получение всех рецензий пользователя
    """
    return await review_service.get_user_reviews(Authorize, skip, limit)


@router.put("/{movie_id}")
async def update_review(
        movie_id: UUID,
        review_update: ReviewUpdate,
        review_service: ReviewService = Depends(get_review_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Обновление рецензии на фильм
    """
    return await review_service.update_review(movie_id, review_update, Authorize)


@router.patch("/{movie_id}")
async def patch_review(
        movie_id: UUID,
        review_update: ReviewPartialUpdate,
        review_service: ReviewService = Depends(get_review_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Частичное обновление рецензии на фильм
    """
    return await review_service.patch_review(movie_id, review_update, Authorize)


@router.delete("/{movie_id}")
async def delete_review(
        movie_id: UUID,
        review_service: ReviewService = Depends(get_review_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Удаление рецензии на фильм
    """
    return await review_service.delete_review(movie_id, Authorize)
