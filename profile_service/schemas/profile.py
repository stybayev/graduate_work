from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator, constr


class ProfileBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    full_name: str = Field(..., min_length=1, max_length=255)

    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.replace('+', '').isdigit():
            raise ValueError('Номер телефона должен содержать только цифры')
        return v


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileInDB(ProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Profile(ProfileInDB):
    pass


class ProfilePartialUpdate(BaseModel):
    phone_number: str | None = Field(None, min_length=10, max_length=15)
    full_name: str | None = Field(None, min_length=1, max_length=255)

    @validator('phone_number')
    def validate_phone(cls, v):
        if v is not None and not v.replace('+', '').isdigit():
            raise ValueError('Номер телефона должен содержать только цифры')
        return v


class PublicProfile(Profile):
    pass