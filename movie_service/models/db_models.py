import uuid
from datetime import datetime

from beanie import Document
from sqlalchemy import ARRAY, Column, DateTime, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from movie_service.db.postgres import Base


class Film(Base):
    __tablename__ = "film_work"
    __table_args__ = {"schema": "movie"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), unique=True)
    title = Column(String(255), nullable=False)
    imdb_rating = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    genre = Column(ARRAY(String), nullable=False)
    actors_names = Column(ARRAY(String), nullable=False)
    writers_names = Column(ARRAY(String), nullable=False)
    director = Column(String(255), nullable=False)
    created = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<Film film_id={self.id}, title={self.title}>"


class reviewsCollection(Document):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    text: str
    created_at: datetime

    class Settings:
        collection = 'reviewsCollection'
