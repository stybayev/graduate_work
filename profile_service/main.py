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


from integrations.kafka import get_kafka_producer, send_to_kafka

def test_send_event():
    topic = "click-events"
    key = "test-user"
    value = {
        "event_type": "click",
        "timestamp": "2024-12-23T10:00:00Z",
        "data": {"button": "submit"},
        "source": "web"
    }

    with get_kafka_producer() as producer:
        send_to_kafka(producer, topic, key, value)
    print("Message sent successfully!")

test_send_event()

