from dataclasses import dataclass
from typing import Literal
from datetime import datetime

_ALLOWED_ROLES = {"system", "user", "assistant"}

@dataclass
class ChatMessage:
	role: Literal["system", "user", "assistant"]
	content: str

	def __post_init__(self):
		if self.role not in _ALLOWED_ROLES:
			raise ValueError(f"Invalid role: {self.role}")

@dataclass
class BDMessage:
	id: int
	user_id: int
	role: Literal["system", "user", "assistant"]
	content: str
	created_at: datetime

	def __post_init__(self):
		if self.role not in _ALLOWED_ROLES:
			raise ValueError(f"Invalid role: {self.role}")