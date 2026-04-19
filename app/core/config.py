from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from pydantic import Field

class Settings(BaseSettings):
	"""Класс для чтения и хранения конфигурации приложения"""
	model_config = SettingsConfigDict(env_file=".env",
	                                  env_prefix="")

	APP_NAME: str = "llm-p"
	ENV: str = "local"

	SQLITE_PATH: str = "./app.db"
	DATABASE_DRIVER: str = "sqlite+aiosqlite"

	JWT_SECRET: str
	JWT_ALG: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, gt=0)

	OPENROUTER_API_KEY: str
	OPENROUTER_BASE_URL: AnyUrl
	OPENROUTER_MODEL: str
	OPENROUTER_SITE_URL: AnyUrl
	OPENROUTER_APP_NAME: str

	@property
	def database_url(self) -> str:
		"""Формирование строки подключения к базе данных"""
		return f"{self.DATABASE_DRIVER}:///{self.SQLITE_PATH}"

settings = Settings()

