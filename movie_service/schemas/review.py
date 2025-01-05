from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from movie_service.models.base_model import PaginatedParams


class Review(BaseModel):
    user_id: UUID
    movie_id: UUID
    text: str
    created_at: datetime


class ReviewsDto(PaginatedParams, Review):
    pass
