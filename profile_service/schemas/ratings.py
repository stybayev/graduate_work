from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class RatingBase(BaseModel):
    movie_id: UUID
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    id: str
    user_id: UUID
    created_at: datetime


class RatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")


class RatingsList(BaseModel):
    ratings: List[RatingResponse]
    total: int


class MovieAverageRating(BaseModel):
    movie_id: UUID
    average_rating: float
    total_ratings: int
