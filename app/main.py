from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

from app.api.routes_chat import chat_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=5.0),
        limits=httpx.Limits(max_keepalive_connections=5)
    ) as client:
        app.state.http_client = client
        yield

def create_app() -> FastAPI:

    app = FastAPI(lifespan=lifespan, title=settings.APP_NAME)
    app.include_router(chat_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": settings.ENV}

    return app

app = create_app()