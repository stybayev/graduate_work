from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from movie_service.models.base_model import SearchParams
from movie_service.models.db_models import Film, reviewsCollection
from movie_service.schemas.film import FilmDto
from movie_service.schemas.review import ReviewsDto
from movie_service.services.base import RepositoryPostgres, RepositoryMongo


class FilmRepository(RepositoryPostgres[Film]):
    ...


class ReviewsRepository(RepositoryMongo[reviewsCollection, ReviewsDto]):
    ...


class FilmServiceABC(ABC):
    @abstractmethod
    async def get_film(self, film_id: UUID) -> FilmDto:
        ...

    @abstractmethod
    async def get_reviews(
            self,
            film_id: UUID,
            params: SearchParams
    ) -> ReviewsDto:
        ...


class FilmService(FilmServiceABC):
    def __init__(
            self,
            film_repository: FilmRepository,
            reviews_repository: ReviewsRepository
    ):
        self.film_repository = film_repository
        self.reviews_repository = reviews_repository

    async def get_film(self, film_id: UUID) -> FilmDto or None:
        """
        Получение информации о фильме по его идентификатору
        :param film_id: UUID фильма
        :return: подробное описание фильма или None
        """
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

    async def get_reviews(self, film_id: UUID, params: SearchParams) -> List[ReviewsDto] or None:
        """
        Получение отзывов по идентификатору фильма
        :param film_id: UUID фильма
        :param params: поисковые параметры, номер страницы и число выводимых результатов запроса
        :return: список отзывов о фильме или None
        """
        reviews = await self.reviews_repository.get_multy(film_id, params=params)
        return reviews
