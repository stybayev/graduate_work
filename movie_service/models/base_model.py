from fastapi import Query
from pydantic import BaseModel


class PaginatedParams(BaseModel):
    page_size: int = Query(ge=1, description="Pagination page size")
    page_number: int = Query(ge=1, description="Pagination page number")
