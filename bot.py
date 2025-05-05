import os
import asyncio
from pyrogram import Client
from helper.database import db_init
from handler.start import start_handler
from handler.callback import callback_handler
from plugins.rename import rename_handler

# Initialize MongoDB
db_init()

app = Client("rename_bot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

# Add Handlers
app.add_handler(start_handler)
app.add_handler(callback_handler)
app.add_handler(rename_handler)

async def main():
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
