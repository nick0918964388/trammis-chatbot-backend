from motor.motor_asyncio import AsyncIOMotorClient
from .models import ChatHistory, ChatHistoryCreate, ChatHistoryUpdate
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

async def update_chat_history(chat_id: str, chat_history: ChatHistoryUpdate) -> ChatHistory:
    update_data = chat_history.dict(exclude_unset=True)
    result = await db.chat_histories.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        return None
    updated_chat_history = await db.chat_histories.find_one({"_id": ObjectId(chat_id)})
    return ChatHistory(**updated_chat_history)