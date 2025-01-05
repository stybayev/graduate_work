from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, List
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from movie_service.models.base_model import BaseModel
from movie_service.models.base_model import SearchParams, PaginatedParams

ModelType = TypeVar("ModelType", bound=BaseModel)
PaginatedModel = TypeVar("PaginatedModel", bound=PaginatedParams)


class Repository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        ...

    async def get_multy(self, *args, **kwargs):
        ...


class RepositoryPostgres(Repository, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            db: AsyncSession
    ):
        self._model = model
        self.db = db

    async def get(self, film_id: UUID) -> Type[ModelType] or None:
        statement = select(self._model).where(self._model.id == film_id)
        results = await self.db.execute(statement=statement)

        return results.scalar_one_or_none()

    async def get_multy(self):
        pass


class RepositoryMongo(Repository, Generic[ModelType, PaginatedModel]):
    def __init__(
            self,
            model: Type[ModelType],
            paginated_model: Type[PaginatedModel],
            client: AsyncIOMotorClient,
    ):
        self._model = model
        self.paginated_model = paginated_model
        self.client = client

    async def get(self):
        pass

    async def get_multy(
            self,
            film_id: UUID,
            params: SearchParams
    ) -> List[Type[PaginatedModel]] or None:
        offset = params.page_size * params.page_number - params.page_size
        data = await self._model.find(
            self._model.movie_id == film_id
        ).skip(offset).limit(params.page_size).to_list()
        models = []
        for entity in data:
            models.append(
                self.paginated_model(
                    **entity.__dict__,
                    page_size=params.page_size,
                    page_number=params.page_number
                )
            )
        return models
