from fastapi.responses import ORJSONResponse
from fastapi import FastAPI

from core.config import settings, JWTSettings
from contextlib import asynccontextmanager
from api.v1 import profiles, bookmarks, ratings, reviews
from async_fastapi_jwt_auth import AuthJWT

from db.mongo import shard_collections
from utils.wait_for_mongo_ready import wait_for_mongo_ready
from utils.enums import ShardedCollections


@asynccontextmanager
async def lifespan(app: FastAPI):
    AuthJWT.load_config(lambda: JWTSettings())
    await wait_for_mongo_ready(settings.mongo_db.url)
    await shard_collections(ShardedCollections)
    yield


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/profile/openapi",
    openapi_url="/api/profile/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["bookmarks"])
app.include_router(ratings.router, prefix="/api/v1/ratings", tags=["ratings"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])
