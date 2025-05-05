from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import WELCOME_IMAGE

start_handler = Client.on_message(filters.command("start"))

@start_handler
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=WELCOME_IMAGE,
        caption="Welcome to the Tensai Rename Bot! 🎬\n\nSend me any video or file to rename it.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Help", callback_data="help")]]
        )
    )
