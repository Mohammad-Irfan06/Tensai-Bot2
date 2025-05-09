from pyrogram import Client, filters
from pyrogram.types import Message
from config import WELCOME_IMAGE

@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_photo(photo=WELCOME_IMAGE, caption="Welcome to the Tensai Rename Bot!")
