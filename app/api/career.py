from fastapi import APIRouter, Depends, HTTPException, status
from ..core.dependencies import get_current_user
from ..services.career import CareerCounselor
from pydantic import BaseModel
from ..models.messages import SystemMessage

router = APIRouter()
counselor = CareerCounselor()

class ChatMessage(BaseModel):
    message: str
    system_message: SystemMessage = None

@router.post("/chat")
async def chat_with_counselor(
    chat: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    try:
        response = counselor.get_chat_response(
            chat.message,
            current_user,
            system_message=chat.system_message
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/chat-history")
async def get_chat_history(
    current_user: dict = Depends(get_current_user)
):
    try:
        history = counselor.get_chat_history(current_user)
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 