from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.profile import Profile, ProfileCreate, ProfileUpdate
from services.profile import ProfileService

from services.profile import get_profile_service

router = APIRouter()


@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile: ProfileCreate,
        service: ProfileService = Depends(get_profile_service)
):
    """Create new user profile"""
    return await service.create_profile(profile)


@router.get("/{user_id}", response_model=Profile)
async def get_profile(
        user_id: UUID,
        service: ProfileService = Depends(get_profile_service)
):
    """Get user profile by user_id"""
    profile = await service.get_profile(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден"
        )
    return profile
#
#
# @router.put("/{user_id}", response_model=Profile)
# async def update_profile(
#         user_id: UUID,
#         profile: ProfileUpdate,
#         service: ProfileService = Depends(get_profile_service)
# ):
#     """Update user profile"""
#     return await service.update_profile(user_id, profile)
#
#
# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_profile(
#         user_id: UUID,
#         service: ProfileService = Depends(get_profile_service)
# ):
#     """Delete user profile"""
#     if not await service.delete_profile(user_id):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Profile not found"
#         )
