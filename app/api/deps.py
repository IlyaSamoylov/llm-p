from fastapi import Depends, Request

from app.usecases.chat import ChatUsecases
from app.repositories.chat_messages import MsgsRepo
from app.services.openrouter_client import OpenRouterClient

async def get_current_uid():
	return 1


async def get_http_client(request: Request):
	return request.app.state.http_client

async def get_openrouter_client(http_client = Depends(get_http_client)) -> OpenRouterClient:
	return OpenRouterClient(client=http_client)

async def get_repo() -> MsgsRepo:
	return MsgsRepo()

async def get_chat_usecase(repo: MsgsRepo = Depends(get_repo),
                           client: OpenRouterClient = Depends(get_openrouter_client)) -> ChatUsecases:
	return ChatUsecases(repo, client)