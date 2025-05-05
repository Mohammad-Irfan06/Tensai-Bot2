import os

API_ID = int(os.getenv("21786970"))
API_HASH = os.getenv("aa1eaa84080fdf706c5cb37a27d35e81")
BOT_TOKEN = os.getenv("7849794082:AAEhUjqhZS-YMrWKgWghLbZnivv3MnRR_Lo")

MONGO_DB_URI = os.getenv("mongodb+srv://mohammadirfan5227:uwkiGejZGyRLV3nP@cluster0.ub1brgf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "/usr/bin/ffmpeg")

# Temporary Download Path
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")

# Welcome Image Path
WELCOME_IMAGE = os.getenv("WELCOME_IMAGE", "./resources/start_pic.jpg")

# Owner and Force Subscribe Channel
OWNER_ID = int(os.getenv("5944299635"))  # Telegram user ID of the bot owner
FORCE_SUB_CHANNEL = os.getenv("KMovieHubHindi")  # username of your updates channel without @
