import httpx

from app.core.config import Settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
	def __init__(self, client: httpx.AsyncClient, conf_settings: Settings):
		self._client = client
		self._settings = conf_settings
		self._model = self._settings.OPENROUTER_MODEL
		self._referer = self._settings.OPENROUTER_SITE_URL
		self._title = self._settings.OPENROUTER_APP_NAME
		self._base_url = self._settings.OPENROUTER_BASE_URL
		self._url = f"{self._base_url}/chat/completions" #TODO: стоит ли выносить в config?
		self._access_token = self._settings.OPENROUTER_API_KEY

	async def chat(self, messages: list[dict[str, str]], temperature: float | None = None) -> str:
		"""Асинхронный метод отправки сообщения по API в OpenRouter"""

		headers = {
			"Authorization": f"Bearer {self._access_token}",
			"Content-Type": "application/json",
			"HTTP-Referer": self._referer,
			"X-Title": self._title
		}
		payload = {
			"model": self._model,
			"messages": messages
		}

		if temperature is not None:
			payload["temperature"] = temperature

		try:
			response = await self._client.post(self._url, json=payload, headers=headers)
			response.raise_for_status()
		except httpx.HTTPStatusError as e: #TODO: импортировать доменные ошибки
			raise ExternalServiceError(f"OpenRouter error: {e.response.text}")
		except httpx.RequestError as e:
			raise ExternalServiceError(f"Connection error: {str(e)}")

		data = response.json()
		try:
			return data["choices"][0]["message"]["content"]
		except (KeyError, IndexError):
			raise ExternalServiceError("Invalid response format from OpenRouter")

#TODO: не забыть собрать message list и добавить system в usecase методе
#TODO: не забыть добавить в `app/core/errors.py` доменные ошибки и сюда импортировать
