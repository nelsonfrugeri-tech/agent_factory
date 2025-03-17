import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from src.domain.file import File
from src.domain.vector import Vector


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    vector: Optional[Vector] = None
    files: List[File] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
