from pydantic import BaseModel
from typing import List, Dict, Any


class MessageRequest(BaseModel):
    role: str
    content: str


class ToolRequest(BaseModel):
    type: str
    index: List[str]


class ChatMessageRequest(BaseModel):
    message: MessageRequest
    tools: List[ToolRequest]
