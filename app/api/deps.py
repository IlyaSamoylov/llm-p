from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.usecases.chat import ChatUsecases
from app.repositories.chat_messages import MsgsRepo
from app.services.openrouter_client import OpenRouterClient
from app.db.session import AsyncSessionLocal

async def get_current_uid():
	return 1

async def get_session() -> AsyncGenerator[AsyncSession, None]:
	async with AsyncSessionLocal() as session:
		yield session

async def get_http_client(request: Request):
	return request.app.state.http_client

async def get_openrouter_client(http_client = Depends(get_http_client)) -> OpenRouterClient:
	return OpenRouterClient(client=http_client)

async def get_repo(session: AsyncSession = Depends(get_session)) -> MsgsRepo:
	return MsgsRepo(session)

async def get_chat_usecase(repo: MsgsRepo = Depends(get_repo),
                           client: OpenRouterClient = Depends(get_openrouter_client)) -> ChatUsecases:
	return ChatUsecases(repo, client)