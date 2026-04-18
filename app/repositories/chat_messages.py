from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db.models import ChatMessage
from app.domain.chat import ChatMessageDomain

class MsgsRepo:
	def __init__(self, session: AsyncSession):
		self._session = session

	async def get_history(self, user_id: int, max_history: int | None = None) -> list[ChatMessageDomain]:
		"""Получение истории диалога"""
		query = (
			select(ChatMessage)
		    .where(ChatMessage.user_id == user_id)
	        .order_by(ChatMessage.created_at.desc()))

		if max_history is not None:
			query = query.limit(max_history)

		result = await self._session.execute(query)

		rows = list(result.scalars().all())
		rows.reverse()
		return [ChatMessageDomain(role=row.role, content=row.content) for row in rows]

	async def add_msg(self, user_id: int, message: ChatMessageDomain):
		"""Добавление сообщения в историю"""
		msg = ChatMessage(user_id=user_id, role=message.role, content=message.content)
		self._session.add(msg)
		await self._session.commit()

	async def delete_history(self, user_id: int):
		"""Удаление истории"""
		await self._session.execute(delete(ChatMessage).where(ChatMessage.user_id == user_id))
		await self._session.commit()
