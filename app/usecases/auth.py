from app.repositories.users import UserRepo
from app.core.errors import ResourceConflictError, AuthenticationError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token

class AuthUsecase:
	"""Бизнес-логика регистрации и авторизации пользователей"""
	def __init__(self, user_repo: UserRepo):
		self._user_repo = user_repo

	async def register(self, email: str, password: str, role: str = "user"):
		"""Метод регистрации пользователя"""
		existing = await self._user_repo.get_user_by_email(email)
		if existing:
			raise ResourceConflictError("Пользователь с таким email уже существует")

		hashed = hash_password(password)
		user = await self._user_repo.create_user(email, hashed, role)
		return user

	async def login(self, email: str, password: str) -> str:
		"""Метод авторизации пользователя"""
		user = await self._user_repo.get_user_by_email(email)
		if not user or not verify_password(password, user.password_hash):
			raise AuthenticationError("Неверный email или пароль")

		return create_access_token(user.id, user.role)

	async def get_profile(self, user_id: int):
		"""Получение профиля пользователя"""
		user = await self._user_repo.get_user_by_id(user_id)
		if not user:
			raise NotFoundError("Пользователь не найден")
		return user