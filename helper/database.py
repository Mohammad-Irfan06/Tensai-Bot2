from motor.motor_asyncio import AsyncIOMotorClient
import os

client = None
db = None

def db_init():
    global client, db
    client = AsyncIOMotorClient(os.getenv("MONGO_DB_URI"))
    db = client.rename_bot

async def save_file_path(user_id, file_path):
    await db.files.update_one(
        {"user_id": user_id},
        {"$set": {"file_path": file_path}},
        upsert=True
    )

async def get_file_path(user_id):
    file = await db.files.find_one({"user_id": user_id})
    return file["file_path"] if file else None
