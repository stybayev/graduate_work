from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID
from utils.enums import BookmarkType


class Bookmark(BaseModel):
    movie_id: UUID
    bookmark_type: BookmarkType = Field(default=BookmarkType.WATCHLIST)


class BookmarkResponse(BaseModel):
    bookmark_id: str
    movie_id: UUID
    bookmark_type: BookmarkType
    created_at: datetime
    updated_at: datetime


class BookmarksListResponse(BaseModel):
    bookmarks: List[BookmarkResponse]
    total: int


class BookmarkUpdate(BaseModel):
    bookmark_type: BookmarkType | None = None
