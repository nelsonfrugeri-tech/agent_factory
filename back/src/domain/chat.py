from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4


class Tool(BaseModel):
    type: str
    index: List[str]


class Message(BaseModel):
    role: str
    content: str


class Question(BaseModel):
    message: Message
    tools: List[Tool]


class Answer(BaseModel):
    message: Message


class Conversation(BaseModel):
    question: Question
    answer: Optional[Answer] = None


class Chat(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    conversations: List[Conversation] = Field(default_factory=list)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now())
