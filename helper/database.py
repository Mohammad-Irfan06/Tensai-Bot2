from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_DB_URI)
db = client[config.DB_NAME]

def store_rename(user_id, old_name, new_name):
    db[config.COLLECTION_NAME].insert_one({"user": user_id, "old_name": old_name, "new_name": new_name})
