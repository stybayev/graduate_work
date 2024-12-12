from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from ..schema import users as schema_user
from ..models import users as model_user


def create_user_profile(db: Session, profile: schema_user.UserProfileCreate):
    db_profile = model_user.User(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


# def get_user_profiles(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(model_user.User).offset(skip).limit(limit).all()

async def get_user_profiles(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(model_user.User).offset(skip).limit(limit))
    return result.scalars().all()


def get_user_profile(db: Session, user_id: int):
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()


def update_user_profile(db: Session, user_id: int, profile: schema_user.UserProfileUpdate):
    db_profile = db.query(model_user.User).filter(model_user.User.id == user_id).first()
    if db_profile:
        for key, value in profile.dict().items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile


def delete_user_profile(db: Session, user_id: int):
    db_profile = db.query(model_user.User).filter(model_user.User.id == user_id).first()
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return db_profile
