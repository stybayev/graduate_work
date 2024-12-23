from abc import ABC, abstractmethod
from uuid import UUID

from movie_service.models.db_models import Film
from movie_service.schemas.film import FilmDto
from movie_service.services.base import RepositoryPostgres


class FilmRepository(RepositoryPostgres[Film, FilmDto]):
    ...


class FilmServiceABC(ABC):
    @abstractmethod
    async def get_film(self, user_id: UUID) -> FilmDto:
        ...


class FilmService(FilmServiceABC):
    def __init__(
            self,
            film_repository: FilmRepository,
    ):
        self.film_repository = film_repository

    async def get_film(self, film_id: UUID) -> FilmDto or None:
        film = await self.film_repository.get(film_id)
        if not film:
            return None
        return FilmDto(
            title=film.title,
            actors_names=film.actors_names,
            director=film.director,
            imdb_rating=film.imdb_rating,
            description=film.description,
            writers_names=film.writers_names,
            created=film.created,
            id=film.id,
            genre=film.genre
        )
