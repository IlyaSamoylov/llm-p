from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

from app.db.base import Base
from app.db.session import engine
from app.api.routes_chat import chat_router
from app.api.routes_auth import auth_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=5.0),
        limits=httpx.Limits(max_keepalive_connections=5)
    ) as client:
        # сохранение единого для приложения асинхронного клиента
        app.state.http_client = client

        # создание таблиц бд
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, title=settings.APP_NAME)
    app.include_router(chat_router)
    app.include_router(auth_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": settings.ENV}

    return app

app = create_app()