from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import WELCOME_IMAGE  # Import the WELCOME_IMAGE from config.py

# The /start command handler
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    # Send the welcome photo and message with a help button
    await message.reply_photo(
        photo=WELCOME_IMAGE,  # The path to the welcome image from config
        caption="Welcome to the Tensai Rename Bot! 🎬\n\nSend me any video or file to rename it.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Help", callback_data="help")]]  # A button for help
        )
    )
