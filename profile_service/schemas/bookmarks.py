from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from utils.enums import BookmarkType


class Bookmark(BaseModel):
    movie_id: str
    bookmark_type: BookmarkType = Field(default=BookmarkType.WATCHLIST)
    note: str | None = None
    rating: int | None = Field(None, ge=1, le=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BookmarkResponse(BaseModel):
    bookmark_id: str
    movie_id: str
    bookmark_type: BookmarkType
    created_at: datetime


class BookmarksListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    total: int
