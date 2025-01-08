from fastapi import Query
from pydantic import BaseModel
from typing import Optional


class PaginatedParams(BaseModel):
    page_size: int = Query(5, ge=1, description="Pagination page size")
    page_number: int = Query(1, ge=1, description="Pagination page number")


class SearchParams(PaginatedParams):
    sort: Optional[str]
