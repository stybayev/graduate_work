from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movie_service.db.postgres import get_db_session
from movie_service.dependencies.registrator import add_factory_to_mapper
from movie_service.models.db_models import Film
from movie_service.services.films import FilmServiceABC, FilmService, FilmRepository


@add_factory_to_mapper(FilmServiceABC)
@cache
def get_film_service(
        session: AsyncSession = Depends(get_db_session),
) -> FilmService:
    return FilmService(
        film_repository=FilmRepository(Film, db=session)
    )
