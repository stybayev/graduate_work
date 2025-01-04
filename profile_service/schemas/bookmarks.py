from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4


class Bookmark(BaseModel):
    movie_id: str


class BookmarkResponse(BaseModel):
    bookmark_id: str


class BookmarksListResponse(BaseModel):
    bookmarks: List[Bookmark]
