from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class FilmDto(BaseModel):
    id: UUID
    title: str
    description: str
    imdb_rating: float
    genre: List[str]
    actors_names: List[str]
    writers_names: List[str]
    director: str
    created: datetime
