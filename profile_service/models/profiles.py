import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base

class UserProfile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "profiles_service"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    phone_number = Column(String(15), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, user_id: uuid.UUID, phone_number: str, full_name: str):
        self.user_id = user_id
        self.phone_number = phone_number
        self.full_name = full_name

    def __repr__(self):
        return f"<UserProfile user_id={self.user_id}, phone_number={self.phone_number}>"
