import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schema.users import UserCreate, UserResponse
from db.postgres import get_db_session
from models.users import User

router = APIRouter()

# Create a user
@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    # Check if the email already exists
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# Get a user by ID
@router.get("/{user_id}", response_model=UserResponse)
async def read_user_endpoint(user_id: uuid.UUID, db: AsyncSession = Depends(get_db_session)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: uuid.UUID, user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


# Delete a user
@router.delete("/{user_id}", response_model=dict)
async def delete_user_endpoint(user_id: uuid.UUID, db: AsyncSession = Depends(get_db_session)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}
