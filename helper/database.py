from pymongo import MongoClient
import config

def connect_to_mongo():
    """Establishes MongoDB connection with error handling."""
    try:
        client = MongoClient(config.MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        db = client[config.DB_NAME]
        db[config.COLLECTION_NAME].create_index([("user", 1)])
        print("✅ MongoDB Connection Successful!")
        return db
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        return None

# Initialize database connection
db = connect_to_mongo()

def store_rename(user_id, old_name, new_name):
    """Stores rename history in MongoDB with error handling."""
    if not db:
        print("❌ Error: Database connection unavailable.")
        return

    try:
        db[config.COLLECTION_NAME].update_one(
            {"user": user_id, "old_name": old_name},
            {"$set": {"new_name": new_name}},
            upsert=True  
        )
        print(f"📂 Rename Stored: {old_name} → {new_name}")
    except Exception as e:
        print(f"❌ MongoDB Insert Error: {e}")
