import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class File(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    files: List[File] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
