from functools import lru_cache
from bson import ObjectId
from fastapi import Depends, HTTPException, status

from db.mongo import get_db
from utils.enums import ShardedCollections

from schemas.bookmarks import Bookmark
from async_fastapi_jwt_auth import AuthJWT

from dependencies.auth import get_current_user


class BookmarkService:
    def __init__(self, db):
        self.collection = db[ShardedCollections.BOOKMARKS_COLLECTION.collection_name]

    def to_object_id(self, id_str: str):
        return ObjectId(id_str) if ObjectId.is_valid(id_str) else id_str

    async def add_bookmark(self,
                           bookmark: Bookmark,
                           Authorize: AuthJWT):
        user_id = await get_current_user(Authorize)
        bookmark_dict = bookmark.dict()
        bookmark_dict["user_id"] = str(user_id)
        bookmark_dict["movie_id"] = str(bookmark.movie_id)
        try:
            result = await self.collection.insert_one(bookmark_dict)
            return str(result.inserted_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@lru_cache()
def get_bookmark_service(db=Depends(get_db)) -> BookmarkService:
    return BookmarkService(db)
