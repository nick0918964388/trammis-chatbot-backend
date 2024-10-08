from motor.motor_asyncio import AsyncIOMotorClient
from .models import (
    ChatHistory,
    ChatHistoryCreate,
    ChatHistoryUpdate,
    MessageAppend,
    get_gmt_time,
    UserChatHistories
)
from bson import ObjectId
import uuid


client = AsyncIOMotorClient("mongodb://mongodb:27017")
database = client.chatbot_db
collection = database.chat_histories


async def create_chat_history(chat_history: ChatHistoryCreate):
    document = chat_history.dict()
    document['date'] = get_gmt_time()
    for message in document['messages']:
        message['timestamp'] = get_gmt_time()
    result = await collection.insert_one(document)
    return await get_chat_history(str(result.inserted_id))


async def get_chat_history(chat_id: str):
    chat = await collection.find_one({"_id": ObjectId(chat_id)})
    if chat:
        chat["id"] = str(chat["_id"])
        if "user_id" not in chat:
            chat["user_id"] = "unknown"  # 为旧数据添加默认user_id
        return ChatHistory(**chat)


async def get_all_chat_histories():
    cursor = collection.find()
    chats = []
    async for chat in cursor:
        chat["id"] = str(chat["_id"])
        if "user_id" not in chat:
            chat["user_id"] = "unknown"  # 为旧数据添加默认user_id
        chats.append(ChatHistory(**chat))
    return chats


async def update_chat_history(
    chat_id: str, chat_history: ChatHistoryUpdate
) -> ChatHistory:
    update_data = chat_history.dict(exclude_unset=True)
    if 'messages' in update_data:
        for message in update_data['messages']:
            if 'timestamp' not in message:
                message['timestamp'] = get_gmt_time()
    result = await collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        return None
    return await get_chat_history(chat_id)


async def append_message_to_chat_history(
    chat_id: str, message: MessageAppend
) -> ChatHistory:
    new_message = message.dict()
    new_message["id"] = str(uuid.uuid4())
    new_message["timestamp"] = get_gmt_time()
    
    result = await collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$push": {"messages": new_message}}
    )
    
    if result.modified_count == 0:
        return None
    
    return await get_chat_history(chat_id)


async def delete_chat_history(chat_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(chat_id)})
    return result.deleted_count > 0


async def get_user_chat_histories(user_id: str) -> UserChatHistories:
    cursor = collection.find({"user_id": user_id})
    chat_histories = []
    async for chat in cursor:
        chat["id"] = str(chat["_id"])
        chat_histories.append(ChatHistory(**chat))
    return UserChatHistories(user_id=user_id, chat_histories=chat_histories)