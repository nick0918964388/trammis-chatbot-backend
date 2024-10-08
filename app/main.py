from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatHistory, ChatHistoryCreate, ChatHistoryUpdate, ChatHistoryAppend
from .database import (
    create_chat_history,
    get_chat_history,
    get_all_chat_histories,
    update_chat_history,
    append_message_to_chat_history,
    delete_chat_history
)
from typing import List

app = FastAPI(
    title="我的聊天历史API",
    description="这是一个管理聊天历史的API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat-history", response_model=ChatHistory)
async def save_chat_history(chat_history: ChatHistoryCreate):
    """
    创建新的聊天历史记录。

    - **chat_history**: 要创建的聊天历史记录的详细信息
    
    返回创建的聊天历史记录。
    """
    result = await create_chat_history(chat_history)
    if result:
        return result
    raise HTTPException(status_code=400, detail="Failed to create chat history")

@app.get("/api/chat-history/{chat_id}", response_model=ChatHistory)
async def read_chat_history(chat_id: str):
    result = await get_chat_history(chat_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Chat history not found")


@app.get("/api/chat-history", response_model=List[ChatHistory])
async def read_chat_histories():
    return await get_all_chat_histories()

@app.put("/api/chat-history/{chat_id}", response_model=ChatHistory)
async def append_message_to_chat(chat_id: str, chat_append: ChatHistoryAppend):
    result = await append_message_to_chat_history(chat_id, chat_append.message)
    if result:
        return result
    raise HTTPException(status_code=404, detail="聊天历史记录未找到或更新失败")

@app.delete("/api/chat-history/{chat_id}")
async def remove_chat_history(chat_id: str):
    """
    删除指定的聊天历史记录。

    - **chat_id**: 要删除的聊天历史记录的ID

    如果成功删除，返回成功消息；如果未找到指定的聊天历史记录，返回404错误。
    """
    result = await delete_chat_history(chat_id)
    if result:
        return {"message": "聊天历史记录已成功删除"}
    raise HTTPException(status_code=404, detail="未找到指定的聊天历史记录")