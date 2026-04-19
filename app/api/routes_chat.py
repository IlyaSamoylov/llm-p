from fastapi import APIRouter, Depends, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageOut
from app.api.deps import get_current_user_id, get_chat_usecase
from app.usecases.chat import ChatUsecases
from app.core.errors import ExternalServiceError

chat_router = APIRouter(prefix="/chat", tags=["chat"])

@chat_router.post("", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, user_id: int = Depends(get_current_user_id),
               chat_usecase: ChatUsecases = Depends(get_chat_usecase)) -> ChatResponse:
	"""Отправка сообщений"""
	try:
		answer = await chat_usecase.ask(user_id, prompt=chat_request.prompt,
		                                system=chat_request.system,
		                                max_history=chat_request.max_history,
		                                temperature=chat_request.temperature)
		return ChatResponse(answer=answer)
	except ExternalServiceError as e:
		raise HTTPException(status_code=502, detail=str(e))

@chat_router.get("/history", status_code=200, response_model=list[ChatMessageOut])
async def get_history(user_id: int = Depends(get_current_user_id),
                      chat_usecase: ChatUsecases = Depends(get_chat_usecase)):
	"""История диалога"""
	history = await chat_usecase.get_history(user_id)
	return history

@chat_router.delete("/history", status_code=200)
async def delete_history(user_id: int = Depends(get_current_user_id),
                         chat_usecase: ChatUsecases = Depends(get_chat_usecase)):
	"""Удаление истории"""
	await chat_usecase.delete_history(user_id)
	return {"message": "История удалена"}