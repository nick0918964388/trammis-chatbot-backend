from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatHistory, ChatHistoryCreate
from .database import create_chat_history, get_chat_history, get_all_chat_histories
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat-history", response_model=ChatHistory)
async def save_chat_history(chat_history: ChatHistoryCreate):
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

@app.get("/api/chat-histories", response_model=List[ChatHistory])
async def read_all_chat_histories():
    return await get_all_chat_historie

@app.get("/api/chat-history", response_model=List[ChatHistory])
async def read_chat_histories():
    return await get_all_chat_histories()