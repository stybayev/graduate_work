from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.users import User
from schema.users import UserCreate


async def get_user(db: AsyncSession, user_id: int):
    """Получить пользователя по ID."""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    """Получить пользователя по email."""
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate):
    """Создать нового пользователя."""
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(db: AsyncSession, db_user: User, user_update: UserCreate):
    """Обновить данные пользователя."""
    for key, value in user_update.dict().items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, db_user: User):
    """Удалить пользователя."""
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}