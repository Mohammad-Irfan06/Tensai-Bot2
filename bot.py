import os
import asyncio
from pyrogram import Client
from helper.database import db_init
from handler.start import start
from handler.callback import callback_handler
from plugins.rename import rename_handler
from plugins.thumb import thumb_handler
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize MongoDB
db_init()

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Add Handlers
app.add_handler(callback_handler)
app.add_handler(rename_handler)
app.add_handler(thumb_handler)

async def main():
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
