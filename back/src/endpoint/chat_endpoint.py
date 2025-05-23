from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from src.business.chat_business import ChatBusiness
from src.port.port import chat_business
from src.model.request.chat_message_request import ChatMessageRequest, ToolRequest
from src.model.response.chat_message_response import MessageResponse
from src.domain.chat import Chat


class ConfigRequest(BaseModel):
    tools: List[ToolRequest]


class CreateChatRequest(BaseModel):
    name: str
    config: ConfigRequest


class ChatResponse(BaseModel):
    id: str
    name: str


chat_router = APIRouter()


@chat_router.post(
    "/v1/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
)
async def create_chat(
    request: CreateChatRequest,
    chat_business: ChatBusiness = Depends(chat_business),
) -> ChatResponse:
    try:
        chat = await chat_business.create(request.name, request.config.tools)
        return ChatResponse(id=chat.id, name=chat.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post(
    "/v1/chat/{uuid}/message",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
)
async def send_message(
    uuid: str,
    request: ChatMessageRequest,
    chat_business: ChatBusiness = Depends(chat_business),
) -> MessageResponse:
    try:
        response = await chat_business.message(uuid, request.message, request.tools)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.get(
    "/v1/chats",
    response_model=List[Chat],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)
async def get_all_chats(
    chat_business: ChatBusiness = Depends(chat_business),
) -> List[Chat]:
    try:
        chats = await chat_business.get_all_chats()
        return chats
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
