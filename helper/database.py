import motor.motor_asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.rename_bot_db

# Collection for storing user thumbnails
thumbnails_collection = db.thumbnails


async def save_thumbnail(user_id: int, thumbnail_path: str):
    """Save the thumbnail path to the database."""
    existing_thumbnail = await thumbnails_collection.find_one({"user_id": user_id})
    
    if existing_thumbnail:
        # Update if thumbnail already exists for user
        await thumbnails_collection.update_one(
            {"user_id": user_id}, {"$set": {"thumbnail_path": thumbnail_path}}
        )
    else:
        # Insert new thumbnail if not found
        await thumbnails_collection.insert_one(
            {"user_id": user_id, "thumbnail_path": thumbnail_path}
        )


async def get_thumbnail(user_id: int):
    """Retrieve the thumbnail path from the database."""
    thumbnail = await thumbnails_collection.find_one({"user_id": user_id})
    return thumbnail["thumbnail_path"] if thumbnail else None
