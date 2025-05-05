from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_SUB_CHANNELS
from pyrogram.errors import UserNotParticipant
from helper.database import add_user
import os

@Client.on_message(filters.command("start"))
async def start_handler(bot, message: Message):
    user = message.from_user

    # Force subscription
    for channel in FORCE_SUB_CHANNELS:
        try:
            await bot.get_chat_member(channel, user.id)
        except UserNotParticipant:
            try:
                invite_link = await bot.create_chat_invite_link(channel, creates_join_request=False)
                return await message.reply_text(
                    f"🔒 To use this bot, please join our channel: [Join Here]({invite_link.invite_link})",
                    disable_web_page_preview=True
                )
            except Exception as e:
                return await message.reply_text(
                    f"⚠️ Error: Cannot create invite link for `{channel}`\n\n`{str(e)}`"
                )

    await add_user(user.id)

    # Buttons
    buttons = [
        [
            InlineKeyboardButton("📋 How to Use", callback_data="how_to_use"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/YourChannel1"),
            InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/YourChannel2")
        ]
    ]

    caption = f"""
👋 **Hi {user.mention}**,  
I'm **Tensai**, your advanced and ultra-fast file renamer bot.  
I support thumbnail embedding, progress tracking, smart UI, and blazing-fast performance!

Just send me any media file and I’ll guide you through renaming it with style!

✨ _Made with ❤️ by Tensai Devs_
"""

    welcome_img_path = "resources/welcome.jpg"
    if os.path.exists(welcome_img_path):
        await message.reply_photo(photo=welcome_img_path, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
