from motor.motor_asyncio import AsyncIOMotorClient
from .models import ChatHistory, ChatHistoryCreate
from bson import ObjectId

client = AsyncIOMotorClient("mongodb://mongodb:27017")
database = client.chatbot_db
collection = database.chat_histories

async def create_chat_history(chat_history: ChatHistoryCreate):
    document = chat_history.dict()
    result = await collection.insert_one(document)
    return await get_chat_history(str(result.inserted_id))

async def get_chat_history(chat_id: str):
    chat = await collection.find_one({"_id": ObjectId(chat_id)})
    if chat:
        chat["id"] = str(chat["_id"])
        return ChatHistory(**chat)

async def get_all_chat_histories():
    cursor = collection.find()
    chats = []
    async for chat in cursor:
        chat["id"] = str(chat["_id"])
        chats.append(ChatHistory(**chat))
    return chats