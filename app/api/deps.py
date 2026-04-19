from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.core.security import decode_access_token
from app.usecases.chat import ChatUsecases
from app.usecases.auth import AuthUsecase
from app.repositories.chat_messages import MsgsRepo
from app.repositories.users import UserRepo
from app.services.openrouter_client import OpenRouterClient
from app.db.session import AsyncSessionLocal
from app.core.errors import AuthenticationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
	"""Получение асинхронной сессии"""
	async with AsyncSessionLocal() as session:
		yield session

async def get_http_client(request: Request):
	"""Получение асинхронного клиента"""
	return request.app.state.http_client

async def get_openrouter_client(http_client = Depends(get_http_client)) -> OpenRouterClient:
	"""Получение экземпляра OpenRouter клиента"""
	return OpenRouterClient(client=http_client)

async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepo:
	"""Получение репо пользователя"""
	return UserRepo(session)

async def get_msg_repo(session: AsyncSession = Depends(get_session)) -> MsgsRepo:
	"""Получение репо сообщений"""
	return MsgsRepo(session)

async def get_chat_usecase(repo: MsgsRepo = Depends(get_msg_repo),
                           client: OpenRouterClient = Depends(get_openrouter_client)) -> ChatUsecases:
	"""Получение экземпляра класса с бизнес логикой чата"""
	return ChatUsecases(repo, client)

async def get_auth_usecase(user_repo: UserRepo = Depends(get_user_repo)) -> AuthUsecase:
	"""Получение экземпляра класса с бизнес-логикой регистрации и логина"""
	return AuthUsecase(user_repo)

async def get_current_user_id(token: str = Depends(oauth2_scheme),
                          user_repo: UserRepo = Depends(get_user_repo)) -> int:
	"""Получение id пользователя по токену"""
	try:
		payload = decode_access_token(token)
		user_id = int(payload.get("sub"))
	except AuthenticationError as e:
		raise HTTPException(status_code=401, detail=str(e))

	user = await user_repo.get_user_by_id(user_id)
	if user is None:
		raise HTTPException(status_code=401, detail="Пользователь не найден")

	return user_id