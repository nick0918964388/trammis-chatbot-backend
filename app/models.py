from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Message(BaseModel):
    id: str
    content: str
    sender: str
    image: str | None = None

class ChatHistoryBase(BaseModel):
    title: str
    date: str = Field(default_factory=lambda: datetime.now().isoformat())
    messages: List[Message]

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistory(ChatHistoryBase):
    id: str

    class Config:
        orm_mode = True