from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from typing import Any

from app.core.config import settings
from app.core.errors import AuthenticationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
	"""Функция хэширования пароля"""
	return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
	"""Верификация пароля"""
	return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: int, role: str = "user") -> str:
	"""Создание JWT токена"""
	iat = datetime.now(timezone.utc)
	exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	payload = {
		"sub": str(user_id),
		"role": role,
		"exp": exp,
		"iat": iat
	}
	return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALG)

def decode_access_token(token: str) -> dict[str, Any]:
	"""Декодирование JWT токена"""
	try:
		return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
	except JWTError:
		raise AuthenticationError("Некорректный токен")