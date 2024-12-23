from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from movie_service.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class Repository(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        ...


class RepositoryPostgres(Repository, Generic[ModelType, CreateSchemaType]):
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
