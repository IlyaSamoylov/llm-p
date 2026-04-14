import httpx

from app.core.config import Settings
from app.core.errors import ExternalServiceError
from app.domain.chat import ChatMessage

class OpenRouterClient:
	def __init__(self, client: httpx.AsyncClient, conf_settings: Settings):
		self._client = client
		self._settings = conf_settings
		self._model = self._settings.OPENROUTER_MODEL
		self._referer = self._settings.OPENROUTER_SITE_URL
		self._title = self._settings.OPENROUTER_APP_NAME
		self._base_url = self._settings.OPENROUTER_BASE_URL
		self._url = f"{self._base_url}/chat/completions"
		self._access_token = self._settings.OPENROUTER_API_KEY

	async def chat(self, messages: list[ChatMessage], temperature: float | None = None) -> ChatMessage:
		"""Асинхронный метод отправки сообщения по API в OpenRouter"""

		headers = {
			"Authorization": f"Bearer {self._access_token}",
			"Content-Type": "application/json",
			"HTTP-Referer": self._referer,
			"X-Title": self._title
		}
		payload: dict[str, object] = {
			"model": self._model,
			"messages": [
				{"role": m.role, "content": m.content} for m in messages
			]
		}

		if temperature is not None:
			payload["temperature"] = temperature

		try:
			response = await self._client.post(self._url, json=payload, headers=headers)
			response.raise_for_status()
		except httpx.HTTPStatusError as e:
			raise ExternalServiceError(f"OpenRouter error: {e.response.text}")
		except httpx.RequestError as e:
			raise ExternalServiceError(f"Connection error: {str(e)}")

		try:
			raw = response.json()
			message = raw["choices"][0]["message"]
			return ChatMessage(role=message["role"], content=message["content"])
		except (KeyError, IndexError, TypeError, ValueError):
			raise ExternalServiceError("Invalid response format from OpenRouter")
