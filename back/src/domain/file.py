from datetime import datetime
from pydantic import BaseModel, Field


class File(BaseModel):
    id: str
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
