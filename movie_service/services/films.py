from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from movie_service.models.base_model import SearchParams
from movie_service.models.db_models import Film, reviewsCollection, ratingsCollection
from movie_service.schemas.film import FilmDto
from movie_service.schemas.ratings import RatingsDto
from movie_service.schemas.review import ReviewsDto
from movie_service.services.base import RepositoryPostgres, RepositoryMongo


class FilmRepository(RepositoryPostgres[Film]):
    ...


class ReviewsRepository(RepositoryMongo[reviewsCollection, ReviewsDto]):
    ...


class RatingsRepository(RepositoryMongo[ratingsCollection, RatingsDto]):
    async def get_avg_rating(self, film_id) -> float | None:
        """
        Процедура получения среднего значения рейтинга у фильма

        :param film_id: идентификатор фильма, по которому хотим получить средний рейтинг
        :return: среднее значение рейтинга фильма
        """
        pipeline = [
            {"$match": {"movie_id": film_id}},
            {
                "$group": {
                    "_id": "$movie_id",
                    "average_rating": {"$avg": "$rating"},
                    "total_ratings": {"$sum": 1}
                }
            }
        ]
        rating = await self._model.aggregate(pipeline).to_list()
        if rating:
            return round(rating.pop()['average_rating'], 2)
        return


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

    @abstractmethod
    async def get_all_ratings(
            self,
            film_id: UUID,
            params: SearchParams
    ) -> RatingsDto:
        ...


class FilmService(FilmServiceABC):
    def __init__(
            self,
            film_repository: FilmRepository,
            reviews_repository: ReviewsRepository,
            ratings_repository: RatingsRepository
    ):
        self.film_repository = film_repository
        self.reviews_repository = reviews_repository
        self.ratings_repository = ratings_repository

    async def get_film(self, film_id: UUID) -> FilmDto or None:
        """
        Получение информации о фильме по его идентификатору
        :param film_id: UUID фильма
        :return: подробное описание фильма или None
        """
        film = await self.film_repository.get(film_id)
        if not film:
            return
        # считаем средний рейтинг фильма
        rating = await self.ratings_repository.get_avg_rating(film_id)

        return FilmDto(
            title=film.title,
            actors_names=film.actors_names,
            director=film.director,
            imdb_rating=rating,
            description=film.description,
            writers_names=film.writers_names,
            created=film.created,
            id=film.id,
            genre=film.genre
        )

    async def get_all_ratings(self, film_id: UUID, params: SearchParams | None) -> List[RatingsDto] or None:
        """
        Получение все выставленных оценок по идентификатору фильма
        :param film_id: UUID фильма
        :param params: поисковые параметры, номер страницы и число выводимых результатов запроса
        :return: список оценок фильма или None
        """
        all_ratings = await self.ratings_repository.get_multy(film_id, params=params)
        return all_ratings

    async def get_reviews(self, film_id: UUID, params: SearchParams) -> List[ReviewsDto] or None:
        """
        Получение отзывов по идентификатору фильма
        :param film_id: UUID фильма
        :param params: поисковые параметры, номер страницы и число выводимых результатов запроса
        :return: список отзывов о фильме или None
        """
        reviews = await self.reviews_repository.get_multy(film_id, params=params)
        return reviews
