import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from movie_service.api.v1.films import router as router_films
from movie_service.core.config import settings
from movie_service.core.logger import LOGGING
from movie_service.dependencies.main import setup_dependencies

app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/movie/openapi",
    openapi_url="/api/movie/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(router_films, prefix="/api/v1/movie", tags=["Get info films"])

setup_dependencies(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
