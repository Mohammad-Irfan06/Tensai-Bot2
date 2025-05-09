import pymongo
from config import MONGO_DB_URI, DB_NAME, COLLECTION_NAME

# Initialize the MongoDB database
def db_init():
    client = pymongo.MongoClient(MONGO_DB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection
