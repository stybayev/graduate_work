from fastapi.responses import ORJSONResponse
from fastapi import FastAPI

from core.config import settings, JWTSettings
from contextlib import asynccontextmanager
from api.v1 import profiles
from async_fastapi_jwt_auth import AuthJWT


@asynccontextmanager
async def lifespan(app: FastAPI):
    AuthJWT.load_config(lambda: JWTSettings())
    yield


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/profile/openapi",
    openapi_url="/api/profile/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])
