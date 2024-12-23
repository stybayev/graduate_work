from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from movie_service.schemas.film import FilmDto
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
