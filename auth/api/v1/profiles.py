from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from auth.db.postgres import get_db_session, engine #, sync_engine
from auth.models.users import Base
from auth.schema.users import UserProfileCreate, UserProfile, UserProfileUpdate
from auth.services import crud

router = APIRouter()
# Base.metadata.create_all(bind=engine)


@router.post("/profiles/", response_model=UserProfile)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db_session)):
    return crud.create_user_profile(db=db, profile=profile)


@router.get("/profiles/", response_model=list[UserProfile])
def read_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    return crud.get_user_profiles(db=db, skip=skip, limit=limit)


@router.get("/profiles/{profile_id}", response_model=UserProfile)
def read_profile(profile_id: int, db: Session = Depends(get_db_session)):
    profile = crud.get_user_profile(db=db, user_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profiles/{profile_id}", response_model=UserProfile)
def update_profile(profile_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db_session)):
    updated_profile = crud.update_user_profile(db=db, user_id=profile_id, profile=profile)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile


@router.delete("/profiles/{profile_id}", response_model=UserProfile)
def delete_profile(profile_id: int, db: Session = Depends(get_db_session)):
    profile = crud.delete_user_profile(db=db, user_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
