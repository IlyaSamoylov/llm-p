from app.domain.chat import ChatMessage, BDMessage
from datetime import datetime, timezone

_STORAGE: list[BDMessage] = []
_ID_SEQ: int = 1

class MsgsRepo:
	def __init__(self):
		self._storage = _STORAGE

	async def get_history(self, user_id: int, max_history: int = -1) -> list[ChatMessage]:

		user_msgs: list[BDMessage] = [msg for msg in self._storage if msg.user_id == user_id]
		user_msgs.sort(key=lambda m: m.created_at)

		if max_history == -1:
			selected = user_msgs
		elif max_history == 0:
			selected = []
		else:
			selected = user_msgs[-max_history:]

		return [ChatMessage(role=m.role, content=m.content) for m in selected]

	async def add_msg(self, user_id: int, message: ChatMessage):
		global _ID_SEQ

		db_msg = BDMessage(id=_ID_SEQ, user_id=user_id, role=message.role,
                            content=message.content, created_at=datetime.now(timezone.utc))
		_ID_SEQ += 1
		self._storage.append(db_msg)

	async def delete_history(self, user_id: int):
		self._storage[:] = [msg for msg in self._storage if msg.user_id != user_id]