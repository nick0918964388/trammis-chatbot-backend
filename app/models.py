from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

def get_gmt_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

class Message(BaseModel):
    id: str
    content: str
    sender: str
    image: Optional[str] = None
    timestamp: str = Field(default_factory=get_gmt_time)

class ChatHistoryBase(BaseModel):
    title: str
    date: str = Field(default_factory=get_gmt_time)
    messages: List[Message]
    user_id: str  # 新增字段，用于记录用户ID

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

class UserChatHistories(BaseModel):
    user_id: str
    chat_histories: List[ChatHistory]