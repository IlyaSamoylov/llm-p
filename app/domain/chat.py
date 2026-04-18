from dataclasses import dataclass
from typing import Literal

_ALLOWED_ROLES = {"system", "user", "assistant"}

@dataclass
class ChatMessageDomain:
	role: Literal["system", "user", "assistant"]
	content: str

	def __post_init__(self):
		if self.role not in _ALLOWED_ROLES:
			raise ValueError(f"Invalid role: {self.role}")

		if not isinstance(self.content, str) or not self.content.strip():
			raise ValueError("Message content must be non-empty string")
