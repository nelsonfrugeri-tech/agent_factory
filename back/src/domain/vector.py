from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from src.domain.file import Project


class Vector(BaseModel):
    id: str
    name: str
    project: Optional[Project] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now())
