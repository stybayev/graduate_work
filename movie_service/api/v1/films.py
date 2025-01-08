from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from movie_service.models.base_model import SearchParams
from movie_service.schemas.film import FilmDto
from movie_service.schemas.ratings import RatingsDto
from movie_service.schemas.review import ReviewsDto
from movie_service.services.films import FilmServiceABC

router = APIRouter()


@router.get("/get_film", response_model=FilmDto)
async def get_film(
        *,
        service: FilmServiceABC = Depends(),
        film_id: UUID
) -> FilmDto or None:
    """
    Получение информации о фильме по идентификатору

    film_id: идентификатор UUID фильма, по которому хотим получить информацию
    """
    film = await service.get_film(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Not found film"
        )
    return film


@router.get("/get_reviews", response_model=List[ReviewsDto])
async def get_reviews(
        *,
        service: FilmServiceABC = Depends(),
        film_id: UUID,
        page_size: int = 5,
        page_number: int = 1,
        sort: str | None = "-created_at",
) -> List[ReviewsDto] or None:
    """
    Получение всех рецензий фильма по идентификатору фильма

    film_id: идентификатор UUID фильма, по которому хотим получить рецензии
    """
    reviews = await service.get_reviews(
        film_id,
        params=SearchParams(
            sort=sort,
            page_size=page_size,
            page_number=page_number
        )
    )
    if not reviews:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="There are no reviews for this film yet"
        )
    return reviews


@router.get("/get_ratings", response_model=List[RatingsDto])
async def get_ratings(
        *,
        service: FilmServiceABC = Depends(),
        film_id: UUID,
        page_size: int = 5,
        page_number: int = 1,
        sort: str | None = "-rating"
) -> List[RatingsDto] or None:
    """
    Получение всех оценок для фильма по идентификатору фильма

    film_id: идентификатор UUID фильма, по которому хотим получить оценки
    """
    ratings = await service.get_all_ratings(
        film_id,
        params=SearchParams(
            page_size=page_size,
            page_number=page_number,
            sort=sort
        )
    )
    if not ratings:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="There are no ratings for this film yet"
        )
    return ratings
