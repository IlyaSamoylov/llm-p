from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env",
	                                  env_prefix="")

	APP_NAME: str = "llm-p"
	ENV: str = "local"

	OPENROUTER_API_KEY: str
	OPENROUTER_BASE_URL: AnyUrl
	OPENROUTER_MODEL: str
	OPENROUTER_SITE_URL: AnyUrl
	OPENROUTER_APP_NAME: str

settings = Settings()

