from app.services.openrouter_client import OpenRouterClient
from app.domain.chat import ChatMessageDomain

class ChatUsecases:
	def __init__(self, repo, client: OpenRouterClient):
		self._repo = repo
		self._client = client

	async def ask(self, user_id: int, prompt: str, system: str | None = None,
	              max_history: int | None = None, temperature: float | None = None):
		messages: list[ChatMessageDomain] = []
		if system:
			messages.append(ChatMessageDomain(role="system", content=system))

		if max_history != 0:
			chat_history: list[ChatMessageDomain] = await self._repo.get_history(user_id, max_history)
			messages.extend(chat_history)

		#TODO: стоит как-то сделать одной транзакцией добавление в историю user-сообщения, получение ответа и добавление его в историю

		new_prompt = ChatMessageDomain(role="user", content=prompt)
		messages.append(new_prompt)
		await self._repo.add_msg(user_id, new_prompt)

		assistant_msg = await self._client.chat(messages, temperature)

		await self._repo.add_msg(user_id, assistant_msg)

		return assistant_msg.content

	async def get_history(self, user_id: int) -> list[ChatMessageDomain]:
		return await self._repo.get_history(user_id)

	async def delete_history(self, user_id):
		await self._repo.delete_history(user_id)
