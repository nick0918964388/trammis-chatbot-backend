from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    id: str
    content: str
    sender: str
    image: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

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

class ChatHistoryUpdate(BaseModel):
    title: Optional[str] = None
    messages: Optional[List[Message]] = None

class MessageAppend(BaseModel):
    content: str
    sender: str
    image: Optional[str] = None

class ChatHistoryAppend(BaseModel):
    message: MessageAppend