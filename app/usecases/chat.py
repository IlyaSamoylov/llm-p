from app.services.openrouter_client import OpenRouterClient
from app.domain.chat import ChatMessage

class ChatUsecases:
	def __init__(self, repo, client: OpenRouterClient):
		self._repo = repo
		self._client = client

	async def ask(self, user_id: str, prompt: str, system: str | None = None, max_history: int = 0,
	              temperature: float | None = None):
		messages: list[ChatMessage] = []
		if system:
			messages.append(ChatMessage(role="system", content=system))

		if max_history > 0:
			chat_history: list[ChatMessage] = await self._repo.get_history(user_id, max_history)
			messages.extend(chat_history)

		new_prompt = ChatMessage(role="user", content=prompt)
		messages.append(new_prompt)

		assistant_msg = await self._client.chat(messages, temperature)

		await self._repo.add_msg(user_id, new_prompt)
		await self._repo.add_msg(user_id, assistant_msg)

		return assistant_msg.content
