from pyrogram import Client
from pyrogram.types import BotCommand
from config import API_ID, API_HASH, BOT_TOKEN
from handler import start, callback
from plugins import rename

bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
)

async def set_commands():
    await bot.set_bot_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "How to use the bot"),
    ])

if __name__ == "__main__":
    bot.run(set_commands())
    bot.run()
