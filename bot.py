import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from helper.database import db_init
from handler.start import start_handler
from handler.callback import callback_handler
from plugins.rename import rename_handler
from plugins.thumb import thumb_handler  # Thumbnail handler

# Initialize MongoDB
db_init()

# Initialize the bot with config variables
app = Client(
    "rename_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Add all handlers
app.add_handler(start_handler)
app.add_handler(callback_handler)
app.add_handler(rename_handler)
app.add_handler(thumb_handler)

async def main():
    await app.start()
    print("Bot started...")  # Optional: helpful for Railway logs
    await idle()             # Keeps the bot running

if __name__ == "__main__":
    from pyrogram.idle import idle  # Import here to avoid circular issues
    asyncio.run(main())
