from pydantic import BaseModel


class MessageResponse(BaseModel):
    response: str
