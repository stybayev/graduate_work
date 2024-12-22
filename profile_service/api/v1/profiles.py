from fastapi import APIRouter, Depends, HTTPException, status, Request

from schemas.profile import (
    Profile, ProfileCreate, ProfileUpdate, ProfilePartialUpdate)
from services.profile import ProfileService
from async_fastapi_jwt_auth import AuthJWT
from services.profile import get_profile_service

from dependencies.auth import security_jwt

router = APIRouter()


@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile: ProfileCreate,
        service: ProfileService = Depends(get_profile_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """Создание профиля пользователя"""
    return await service.create_profile(profile=profile, Authorize=Authorize)


@router.get("/{user_id}", response_model=Profile)
async def get_profile(
        service: ProfileService = Depends(get_profile_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """Получение профиля пользователя по user_id"""
    profile = await service.get_profile(Authorize=Authorize)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден"
        )
    return profile


@router.put("/{user_id}", response_model=Profile)
async def update_profile(
        profile: ProfileUpdate,
        service: ProfileService = Depends(get_profile_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """Обновление профиля пользователя"""
    return await service.update_profile(profile, Authorize)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
        service: ProfileService = Depends(get_profile_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """Удаление профиля пользователя"""
    if not await service.delete_profile(Authorize):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не существует"
        )


@router.patch("/{user_id}", response_model=Profile)
async def patch_profile(
        profile: ProfilePartialUpdate,
        service: ProfileService = Depends(get_profile_service),
        Authorize: AuthJWT = Depends(),
        user: dict = Depends(security_jwt)
):
    """Частичное обновление профиля пользователя"""
    return await service.patch_profile(profile, Authorize)
