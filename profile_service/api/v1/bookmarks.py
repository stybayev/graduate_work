from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.bookmarks import (
    Bookmark,
    BookmarkResponse,
    BookmarksListResponse,
    BookmarkUpdate
)
from services.bookmarks import BookmarkService, get_bookmark_service
from async_fastapi_jwt_auth import AuthJWT
from dependencies.auth import security_jwt
from uuid import UUID
from utils.enums import BookmarkType

router = APIRouter()


@router.post("/bookmark/",
             status_code=status.HTTP_201_CREATED,
             response_model=BookmarkResponse)
async def add_bookmark(
        bookmark: Bookmark,
        service: BookmarkService = Depends(get_bookmark_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Добавление фильма в закладки.
    """
    result = await service.add_bookmark(bookmark, Authorize=Authorize)
    return BookmarkResponse(
        bookmark_id=str(result["_id"]),
        movie_id=result["movie_id"],
        bookmark_type=result["bookmark_type"],
        created_at=result["created_at"],
        updated_at=result["updated_at"]
    )


@router.get("/bookmarks/",
            response_model=BookmarksListResponse)
async def get_bookmarks(
        bookmark_type: BookmarkType = Query(description="Тип закладки",
                                            default=BookmarkType.WATCHLIST,
                                            enum=[BookmarkType.WATCHLIST, BookmarkType.FAVORITE]),
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        service: BookmarkService = Depends(get_bookmark_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Получение списка закладок пользователя.
    """
    return await service.get_user_bookmarks(
        Authorize=Authorize,
        bookmark_type=bookmark_type,
        skip=skip,
        limit=limit
    )


@router.delete("/bookmark/{movie_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def remove_bookmark(
        movie_id: UUID,
        service: BookmarkService = Depends(get_bookmark_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Удаление фильма из закладок.
    """
    await service.remove_bookmark(Authorize=Authorize, movie_id=movie_id)


@router.patch("/bookmark/{movie_id}")
async def update_bookmark(
        movie_id: UUID,
        bookmark: BookmarkUpdate,
        service: BookmarkService = Depends(get_bookmark_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """
    Обновление информации о закладке.
    """
    await service.update_bookmark(
        Authorize=Authorize,
        movie_id=movie_id,
        bookmark_data=bookmark.dict(exclude_unset=True)
    )
    return {"status": "updated"}
