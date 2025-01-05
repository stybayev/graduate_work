from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

from utils.enums import BookmarkType


class Bookmark(BaseModel):
    movie_id: str
    bookmark_type: BookmarkType = Field(default=BookmarkType.WATCHLIST)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BookmarkResponse(BaseModel):
    bookmark_id: str
    movie_id: str
    bookmark_type: BookmarkType
    created_at: datetime


class BookmarksListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    total: int
