from pymongo import MongoClient
import config

# Connect to MongoDB with error handling
try:
    client = MongoClient(config.MONGO_DB_URI)
    db = client[config.DB_NAME]
    db[config.COLLECTION_NAME].create_index([("user", 1)])  # Index for fast queries
    print("✅ MongoDB Connection Successful!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")

# Function to store rename history
def store_rename(user_id, old_name, new_name):
    try:
        db[config.COLLECTION_NAME].update_one(
            {"user": user_id, "old_name": old_name},  # Match existing file rename
            {"$set": {"new_name": new_name}},  # Update with new name
            upsert=True  # Creates entry if it doesn't exist
        )
        print(f"📂 Rename Stored: {old_name} → {new_name}")
    except Exception as e:
        print(f"❌ MongoDB Insert Error: {e}")
