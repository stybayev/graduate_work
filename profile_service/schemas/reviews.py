from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID


class ReviewBase(BaseModel):
    movie_id: UUID
    text: str = Field(..., min_length=10, max_length=10000)
    title: str = Field(..., min_length=3, max_length=255)


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime | None = None


class ReviewUpdate(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)
    title: str = Field(..., min_length=3, max_length=255)


class ReviewsList(BaseModel):
    reviews: List[ReviewResponse]
    total: int


class ReviewPartialUpdate(BaseModel):
    text: str | None = Field(None, min_length=10, max_length=10000)
    title: str | None = Field(None, min_length=3, max_length=255)
