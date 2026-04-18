from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUsecase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ResourceConflictError, AuthenticationError, NotFoundError

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest, auth_usecase: AuthUsecase = Depends(get_auth_usecase)):
	"""Регистрация пользователя"""
	try:
		user = await auth_usecase.register(str(data.email), data.password)
		return user
	except ResourceConflictError as e:
		raise HTTPException(status_code=409, detail=str(e))

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    auth_usecase: AuthUsecase = Depends(get_auth_usecase)):
	"""Авторизация пользователя."""
	try:
		token = await auth_usecase.login(data.username, data.password)
		return TokenResponse(access_token=token)
	except AuthenticationError as e:
		raise HTTPException(status_code=401, detail=str(e))

@auth_router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id),
                 auth_usecase: AuthUsecase = Depends(get_auth_usecase)):
	"""Информация о текущем пользователе"""
	try:
		user = await auth_usecase.get_profile(user_id)
		return user
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))