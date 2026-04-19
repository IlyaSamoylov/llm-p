from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
	"""Модель запроса на регистрацию пользователя"""
	email: EmailStr
	password: str = Field(min_length=5)

class TokenResponse(BaseModel):
	"""Модель возврата токена"""
	access_token: str
	token_type: str = "bearer"