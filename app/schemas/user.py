from pydantic import BaseModel, Field, EmailStr

class UserPublic(BaseModel):
	"""Публичная модель пользователя"""
	id: int = Field(gt=0)
	email: EmailStr
	role: str = Field(default="user")

	model_config = {"from_attributes": True}