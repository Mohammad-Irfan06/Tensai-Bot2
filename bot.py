import os
import time
import logging
from pyrogram import Client, filters
from helper.database import get_thumbnail
from helper.utils import progress_for_pyrogram
from pyrogram.errors import FloodWait
from handler.callback import cancel, rename, upload_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RenameBot")

API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bot.add_handler(cancel)
bot.add_handler(rename)
bot.add_handler(upload_file)

bot.run()
