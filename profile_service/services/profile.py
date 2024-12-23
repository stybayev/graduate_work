from functools import lru_cache
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException, status, Depends
from async_fastapi_jwt_auth import AuthJWT

from models.profiles import UserProfile

from schemas.profile import (ProfileCreate, ProfileUpdate,
                             ProfilePartialUpdate)

from db.postgres import get_db_session

from dependencies.auth import get_current_user


class ProfileService:
    def __init__(
            self,
            db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def get_profile(self,
                          Authorize: AuthJWT) -> UserProfile | None:
        """
        Получение своего профиля пользователя
        """
        user_id = await get_current_user(Authorize)
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_profile_by_phone_number(self, phone_number: UUID) -> UserProfile | None:
        """
        Получение номера телофона по номеру телефона
        """
        query = select(UserProfile).where(UserProfile.phone_number == phone_number)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_public_profile(self, user_id: UUID) -> UserProfile | None:
        """
        Получение публичного профиля пользователя
        """
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    # @access_token_required
    async def create_profile(self,
                             profile: ProfileCreate,
                             Authorize: AuthJWT) -> UserProfile:
        """
       Создание профиля пользователя
        """
        user_id = await get_current_user(Authorize)

        existing_profile = await self.get_profile(Authorize)
        existing_profile_by_phone_number = await self.get_profile_by_phone_number(profile.phone_number)
        if existing_profile or existing_profile_by_phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Профиль уже существует"
            )

        db_profile = UserProfile(**profile.dict(), user_id=user_id)
        self.db_session.add(db_profile)
        await self.db_session.commit()
        await self.db_session.refresh(db_profile)
        return db_profile

    async def update_profile(
            self,
            profile: ProfileUpdate,
            Authorize: AuthJWT
    ) -> UserProfile | None:
        """
        Обновление профиля пользователя
        """
        user_id = await get_current_user(Authorize)
        db_profile = await self.get_profile(Authorize)
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль не существует"
            )

        query = (
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(**profile.dict())
            .returning(UserProfile)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalars().first()

    async def delete_profile(self, Authorize: AuthJWT) -> bool:
        user_id = await get_current_user(Authorize)
        query = delete(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.rowcount > 0

    async def patch_profile(
            self,
            profile_update: ProfilePartialUpdate,
            Authorize: AuthJWT
    ) -> UserProfile | None:
        """
        Частичное обновление профиля пользователя
        """
        user_id = await get_current_user(Authorize)
        db_profile = await self.get_profile(Authorize)
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль не существует"
            )

        # Фильтруем только не-None значения
        update_data = profile_update.dict(exclude_unset=True)
        if not update_data:
            return db_profile

        query = (
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(**update_data)
            .returning(UserProfile)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.scalars().first()


@lru_cache()
def get_profile_service(
        db_session: AsyncSession = Depends(get_db_session),
) -> ProfileService:
    return ProfileService(db_session)
