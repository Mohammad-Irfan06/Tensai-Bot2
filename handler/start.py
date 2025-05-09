from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import WELCOME_IMAGE

# Define start command handler directly on the Client instance
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    try:
        await message.reply_photo(
            photo=WELCOME_IMAGE,  # Ensure WELCOME_IMAGE path or URL is correct in config.py
            caption="Welcome to the Tensai Rename Bot! 🎬\n\nSend me any video or file to rename it.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Help", callback_data="help")]]
            )
        )
    except Exception as e:
        # Handle exceptions if any error occurs while sending photo
        await message.reply_text("Sorry, something went wrong. Please try again later.")
        print(f"Error sending start message: {e}")
