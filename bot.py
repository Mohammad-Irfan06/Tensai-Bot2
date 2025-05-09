import os
import asyncio
from pyrogram import Client
from helper.database import db_init
from handler.start import start  # Import the start function, not start_handler
from handler.callback import callback  # Import the callback function
from plugins.rename import rename  # Import the rename function
from plugins.thumb import thumb  # Import the thumb function
from config import API_ID, API_HASH, BOT_TOKEN  # Import API credentials from config

# Initialize MongoDB
db_init()

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Add Handlers
app.add_handler(Client.on_message(filters.command("start"))(start))  # Use the function directly
app.add_handler(Client.on_callback_query(filters.regex("help"))(callback))  # Use the callback function directly
app.add_handler(rename)  # Add the rename handler directly
app.add_handler(thumb)  # Add the thumb handler directly

async def main():
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
