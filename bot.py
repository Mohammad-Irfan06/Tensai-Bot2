import os
import asyncio
from pyrogram import Client
from helper.database import db_init
from handler.start import start  # Import the start function correctly
from handler.callback import handle_callbacks  # Correct callback import
from plugins.rename import rename_handler
from plugins.thumb import thumb_handler
from config import API_ID, API_HASH, BOT_TOKEN  # Import API credentials from config

# Initialize MongoDB
db_init()

# Initialize the bot with the credentials
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Add Handlers
app.add_handler(rename_handler)
app.add_handler(thumb_handler)
app.add_handler(handle_callbacks)  # Adding the callback handler to bot

async def main():
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
