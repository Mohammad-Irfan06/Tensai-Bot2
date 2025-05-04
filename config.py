import os

API_ID = int(os.environ.get("API_ID", ""))  # Replace with your API_ID
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MONGO_URL = os.environ.get("MONGO_URL", "")  # MongoDB URI
