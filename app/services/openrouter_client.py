import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError
from app.domain.chat import ChatMessageDomain

class OpenRouterClient:
	def __init__(self, client: httpx.AsyncClient):
		self._client = client
		self._model = settings.OPENROUTER_MODEL
		self._referer = str(settings.OPENROUTER_SITE_URL)
		self._title = settings.OPENROUTER_APP_NAME
		self._base_url = str(settings.OPENROUTER_BASE_URL)
		self._url = f"{self._base_url}/chat/completions"
		self._access_token = settings.OPENROUTER_API_KEY

	async def chat(self, messages: list[ChatMessageDomain], temperature: float | None = None) -> ChatMessageDomain:
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
			content = message.get("content")

		except (KeyError, IndexError, TypeError, ValueError):
			raise ExternalServiceError("Invalid response format from OpenRouter")

		if not content or not isinstance(content, str):
			raise ExternalServiceError("LLM returned empty content")

		return ChatMessageDomain(role=message["role"], content=content)
