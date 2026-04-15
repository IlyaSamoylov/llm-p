from app.domain.chat import ChatMessage, BDMessage
from datetime import datetime

class MsgsRepo:
	def __init__(self):
		self._msgs: list[BDMessage] = []
		self._id_seq: int = 1

	async def get_history(self, user_id: int, max_history: int = -1) -> list[ChatMessage]:

		user_msgs: list[BDMessage] = [msg for msg in self._msgs if msg.user_id == user_id]

		user_msgs.sort(key=lambda m: m.created_at)
		if max_history == -1:
			selected = user_msgs
		if max_history == 0:
			selected = []
		else:
			selected = user_msgs[-max_history:]

		return [ChatMessage(role=m.role, content=m.content) for m in selected]

	async def add_msg(self, user_id: int, message: ChatMessage):
		db_msg = BDMessage(id=self._id_seq, user_id=user_id, role=message.role,
                            content=message.content, created_at=datetime.now())
		self._id_seq += 1
		self._msgs.append(db_msg)

	async def delete_history(self, user_id: int):
		self._msgs = [msg for msg in self._msgs if msg.user_id != user_id]