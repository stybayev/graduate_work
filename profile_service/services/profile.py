from functools import lru_cache
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException, status, Depends

from models.profiles import UserProfile

from schemas.profile import ProfileCreate, ProfileUpdate

from db.postgres import get_db_session


class ProfileService:
    def __init__(
            self,
            db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def get_profile(self, user_id: UUID) -> UserProfile | None:
        """
        Получение профиля пользователя по user_id
        """
        query = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def create_profile(self, profile: ProfileCreate) -> UserProfile:
        """
       Создание профиля пользователя
        """
        existing_profile = await self.get_profile(profile.user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Профиль уже существует"
            )

        db_profile = UserProfile(**profile.dict())
        self.db_session.add(db_profile)
        await self.db_session.commit()
        await self.db_session.refresh(db_profile)
        return db_profile

    # async def update_profile(
    #         self, user_id: UUID, profile: ProfileUpdate
    # ) -> UserProfile | None:
    #     """
    #     Обновление профиля пользователя
    #     """
    #     db_profile = await self.get_profile(user_id)
    #     if not db_profile:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Профиль уже существует"
    #         )
    #
    #     query = (
    #         update(UserProfile)
    #         .where(UserProfile.user_id == user_id)
    #         .values(**profile.dict())
    #         .returning(UserProfile)
    #     )
    #     result = await self.db_session.execute(query)
    #     await self.db_session.commit()
    #     return result.scalars().first()
    #
    # async def delete_profile(self, user_id: UUID) -> bool:
    #     query = delete(UserProfile).where(UserProfile.user_id == user_id)
    #     result = await self.db_session.execute(query)
    #     await self.db_session.commit()
    #     return result.rowcount > 0


@lru_cache()
def get_profile_service(
        db_session: AsyncSession = Depends(get_db_session),
) -> ProfileService:
    return ProfileService(db_session)
