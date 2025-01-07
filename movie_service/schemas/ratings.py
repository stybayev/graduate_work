from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from movie_service.models.base_model import PaginatedParams


class Rating(BaseModel):
    user_id: UUID
    movie_id: UUID
    rating: int
    created_at: datetime


class RatingsDto(PaginatedParams, Rating):
    pass
