import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "/usr/bin/ffmpeg")

# Temporary Download Path
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")

# Welcome Image Path
WELCOME_IMAGE = os.getenv("WELCOME_IMAGE", "./resources/start_pic.jpg")
