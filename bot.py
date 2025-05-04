import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RenameBot")

bot = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Rest of your bot code...
bot.run()
