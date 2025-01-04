from fastapi import APIRouter, Depends, HTTPException, status
from schemas.bookmarks import Bookmark, BookmarkResponse, BookmarksListResponse
from services.bookmarks import BookmarkService, get_bookmark_service
from async_fastapi_jwt_auth import AuthJWT

from dependencies.auth import security_jwt

router = APIRouter()


@router.post("/bookmark/",
             status_code=status.HTTP_201_CREATED,
             response_model=BookmarkResponse)
async def add_bookmark(bookmark: Bookmark,
                       service: BookmarkService = Depends(get_bookmark_service),
                       Authorize: AuthJWT = Depends(),
                       user: dict = Depends(security_jwt)
                       ):
    """
    Добавление фильма в закладки.
    """
    bookmark_id = await service.add_bookmark(bookmark, Authorize=Authorize)
    return BookmarkResponse(bookmark_id=bookmark_id)
