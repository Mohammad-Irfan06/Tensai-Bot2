import os
import asyncio
from pyrogram import Client
from helper.database import db_init
from handler.start import start_handler
from handler.callback import callback_handler
from plugins.rename import rename_handler
from plugins.thumb import thumb_handler  # Added thumb_handler to include it in the bot

# Initialize MongoDB
db_init()

app = Client("rename_bot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

# Add Handlers
app.add_handler(start_handler)
app.add_handler(callback_handler)
app.add_handler(rename_handler)
app.add_handler(thumb_handler)  # Added the thumb handler

async def main():
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
