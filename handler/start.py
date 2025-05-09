# handler/start.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import WELCOME_IMAGE

# This function will be triggered when the /start command is called
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    # Send the welcome image with a caption and inline buttons
    await message.reply_photo(
        photo=WELCOME_IMAGE,
        caption="Welcome to the Tensai Rename Bot! 🎬\n\nSend me any video or file to rename it.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Help", callback_data="how_to_use")],
                [InlineKeyboardButton("About", callback_data="about")]
            ]
        )
    )
