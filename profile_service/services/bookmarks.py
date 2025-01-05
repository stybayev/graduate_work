from functools import lru_cache
from fastapi import Depends, HTTPException, status
from datetime import datetime

from db.mongo import get_db
from utils.enums import ShardedCollections
from schemas.bookmarks import Bookmark, BookmarkType, BookmarksListResponse
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import get_current_user


class BookmarkService:
    def __init__(self, db):
        self.collection = db[ShardedCollections.BOOKMARKS_COLLECTION.collection_name]

    async def add_bookmark(self,
                           bookmark: Bookmark,
                           Authorize: AuthJWT) -> Bookmark:

        user_id = await get_current_user(Authorize)

        # Проверяем, не существует ли уже такая закладка
        existing_bookmark = await self.collection.find_one({
            "user_id": str(user_id),
            "movie_id": str(bookmark.movie_id)
        })

        if existing_bookmark:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот фильм уже добавлен в закладки"
            )

        bookmark_dict = bookmark.dict()
        bookmark_dict.update({
            "user_id": str(user_id),
            "movie_id": str(bookmark.movie_id),
            "created_at": datetime.utcnow()
        })

        try:
            result = await self.collection.insert_one(bookmark_dict)
            return str(result.inserted_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_user_bookmarks(
            self,
            Authorize: AuthJWT,
            bookmark_type: BookmarkType = BookmarkType.WATCHLIST,
            skip: int = 0,
            limit: int = 20
    ) -> BookmarksListResponse:

        user_id = await get_current_user(Authorize)
        query = {"user_id": str(user_id)}
        if bookmark_type:
            query["bookmark_type"] = bookmark_type

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        bookmarks = []

        async for doc in cursor:
            bookmarks.append({
                "bookmark_id": str(doc["_id"]),
                "movie_id": doc["movie_id"],
                "bookmark_type": doc["bookmark_type"],
                "created_at": doc["created_at"]
            })

        return BookmarksListResponse(bookmarks=bookmarks, total=total)

    async def remove_bookmark(self, Authorize: AuthJWT,
                              movie_id: str):

        user_id = await get_current_user(Authorize)
        result = await self.collection.delete_one({
            "user_id": str(user_id),
            "movie_id": str(movie_id)
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Закладка не найдена"
            )

        return True

    async def update_bookmark(
            self,
            Authorize: AuthJWT,
            movie_id: str,
            bookmark_data: dict
    ):

        user_id = await get_current_user(Authorize)
        result = await self.collection.update_one(
            {
                "user_id": str(user_id),
                "movie_id": str(movie_id)
            },
            {"$set": bookmark_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Закладка не найдена"
            )

        return True


@lru_cache()
def get_bookmark_service(db=Depends(get_db)) -> BookmarkService:
    return BookmarkService(db)
