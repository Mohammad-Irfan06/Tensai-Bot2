from pyrogram import Client, filters
from pyrogram.types import Message

start_handler = Client.on_message(filters.command("start"))

async def start_handler(client: Client, message: Message):
    await message.reply_text("Welcome to the Rename Bot! Send me a file and I will rename it.")
