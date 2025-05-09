import os
import asyncio
import logging
from pyrogram import Client
from helper.database import db_init
from handler.start import start  # Importing the correct start function
from handler.callback import handle_callbacks  # Corrected handler function name
from plugins.rename import rename_handler
from plugins.thumb import thumb_handler
from config import API_ID, API_HASH, BOT_TOKEN  # Import API credentials from config

# Setting up logging to track errors and events
logging.basicConfig(level=logging.INFO, filename="bot_logs.log", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize MongoDB
db_init()

# Create the Pyrogram client with bot credentials
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register the handlers
@app.on_callback_query()
async def callback_handler(bot, query):
    try:
        await handle_callbacks(bot, query)  # Use the imported callback handler
    except Exception as e:
        logger.error(f"Callback handler error: {e}")
        await query.message.edit_text("An error occurred, please try again later.")

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    try:
        await start(client, message)  # Use the correct start function
    except Exception as e:
        logger.error(f"Start handler error: {e}")
        await message.reply_text("An error occurred while processing your request. Please try again.")

@app.on_message(filters.document)
async def rename_handler(client: Client, message: Message):
    try:
        await rename_handler(client, message)  # Use the correct rename handler
    except Exception as e:
        logger.error(f"Rename handler error: {e}")
        await message.reply_text("An error occurred while renaming your file. Please try again.")

@app.on_message(filters.photo)
async def thumb_handler(client: Client, message: Message):
    try:
        await thumb_handler(client, message)  # Use the correct thumbnail handler
    except Exception as e:
        logger.error(f"Thumbnail handler error: {e}")
        await message.reply_text("An error occurred while processing your thumbnail. Please try again.")

async def main():
    try:
        # Start the bot
        await app.start()
        logger.info("Bot started successfully.")
    except Exception as e:
        logger.error(f"Error while starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
