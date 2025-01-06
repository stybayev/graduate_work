from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class RatingBase(BaseModel):
    movie_id: str
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    id: str
    user_id: str
    created_at: datetime


class RatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")


class RatingsList(BaseModel):
    ratings: List[RatingResponse]
    total: int
