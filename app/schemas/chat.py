from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
	prompt: str = Field(min_length=1)
	system: str | None = None
	max_history: int | None = Field(default=None, ge=0)
	temperature: float | None = Field(default=None, ge=0.0, le=2.0) # если не указан, OpenRouter автоматически поставит 1.0

class ChatResponse(BaseModel):
	answer: str

class ChatMessageOut(BaseModel):
	role: str
	content: str