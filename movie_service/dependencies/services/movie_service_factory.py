from functools import cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession

from movie_service.db.mongo import init_mongo
from movie_service.db.postgres import get_db_session
from movie_service.dependencies.registrator import add_factory_to_mapper
from movie_service.models.db_models import Film, reviewsCollection
from movie_service.schemas.review import ReviewsDto
from movie_service.services.films import FilmServiceABC, FilmService, FilmRepository, ReviewsRepository


@add_factory_to_mapper(FilmServiceABC)
@cache
def get_film_service(
        session: AsyncSession = Depends(get_db_session),
        client: AsyncIOMotorClient = Depends(init_mongo)
) -> FilmService:
    return FilmService(
        film_repository=FilmRepository(Film, db=session),
        reviews_repository=ReviewsRepository(
            model=reviewsCollection,
            paginated_model=ReviewsDto,
            client=client
        )
    )
