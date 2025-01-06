from fastapi import APIRouter, Depends, Query
from schemas.ratings import (
    RatingCreate, RatingResponse,
    RatingUpdate, RatingsList, MovieAverageRating)
from services.ratings import RatingService, get_rating_service
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import security_jwt

router = APIRouter()


@router.post("/rating/",
             response_model=RatingResponse,
             description="Создать рейтинг для фильма")
async def create_rating(
        rating: RatingCreate,
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    result = await service.create_rating(rating, Authorize)
    return RatingResponse(
        id=str(result["_id"]),
        user_id=result["user_id"],
        movie_id=result["movie_id"],
        rating=result["rating"],
        created_at=result["created_at"]
    )


@router.get("/movies/{movie_id}/ratings/",
            response_model=RatingsList,
            description="Получить все рейтинги фильма")
async def get_movie_ratings(
        movie_id: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    return await service.get_movie_ratings(movie_id, skip, limit)


@router.get("/ratings/",
            response_model=RatingsList,
            description="Получить все рейтинги пользователя")
async def get_user_ratings(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    return await service.get_user_ratings(Authorize, skip, limit)


@router.put("/rating/{movie_id}",
            description="Обновить рейтинг фильма")
async def update_rating(
        movie_id: str,
        rating: RatingUpdate,
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    await service.update_rating(movie_id, rating, Authorize)
    return {"status": "updated"}


@router.delete("/rating/{movie_id}",
               description="Удалить рейтинг фильма")
async def delete_rating(
        movie_id: str,
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    await service.delete_rating(movie_id, Authorize)
    return {"status": "deleted"}


@router.get("/movies/{movie_id}/average/",
            response_model=MovieAverageRating,
            description="Получить средний рейтинг фильма")
async def get_movie_average_rating(
        movie_id: str,
        service: RatingService = Depends(get_rating_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    return await service.get_movie_average_rating(movie_id)
