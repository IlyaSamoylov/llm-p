from dataclasses import dataclass
from typing import Literal

_ALLOWED_ROLES = {"system", "user", "assistant"}

@dataclass
class ChatMessageDomain:
	"""Доменная модель сообщения в чате"""
	role: Literal["system", "user", "assistant"]
	content: str

	def __post_init__(self):
		if self.role not in _ALLOWED_ROLES:
			raise ValueError(f"Недопустимое значение роли сообщения: {self.role}")

		if not isinstance(self.content, str) or not self.content.strip():
			raise ValueError("Значение 'content' в сообщении не может быть пустым")
