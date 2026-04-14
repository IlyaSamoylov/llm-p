from app.domain.chat import ChatMessage

class MsgsRepo:
	def __init__(self):
		self._msgs: list[tuple[str, ChatMessage]] = []

	async def get_history(self, user_id: str, max_history: int) -> list[ChatMessage]:
		if max_history <= 0:
			return []

		user_msgs: list[ChatMessage] = [msg for uid, msg in self._msgs if uid == user_id]
		return user_msgs[-max_history:]

	async def add_msg(self, user_id: str, message: ChatMessage):
		self._msgs.append((user_id, message))

	async def delete_history(self, user_id: str):
		self._msgs = [(uid, msg) for uid, msg in self._msgs if uid != user_id]