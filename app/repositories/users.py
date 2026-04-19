from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User

class UserRepo:
	"""Пользовательский Репозиторий"""
	def __init__(self, session: AsyncSession):
		self._session = session

	async def get_user_by_email(self, email: str) -> User | None:
		"""Получение пользователя по email"""
		result = await self._session.execute(select(User).where(User.email == email))
		return result.scalar_one_or_none()

	async def get_user_by_id(self, uid: int) -> User | None:
		"""Получение пользователя по id"""
		result = await self._session.execute(select(User).where(User.id == uid))
		return result.scalar_one_or_none()

	async def create_user(self, email: str, password_hash: str, role: str = "user") -> User:
		"""Создание нового пользователя"""
		user = User(email=email, password_hash=password_hash, role=role)
		self._session.add(user)
		await self._session.commit()
		await self._session.refresh(user)
		return user
