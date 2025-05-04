from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import save_thumbnail
import os
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("set_thumbnail"))
async def set_thumbnail(bot: Client, message: Message):
    user_id = message.from_user.id
    if message.reply_to_message and message.reply_to_message.photo:
        # Save thumbnail in DB
        file_id = message.reply_to_message.photo.file_id
        thumbnail_path = await bot.download_media(file_id)
        
        # Save path in database
        await save_thumbnail(user_id, thumbnail_path)
        await message.reply("Thumbnail has been set successfully!")
    else:
        await message.reply("Please reply to a photo to set it as a thumbnail.")

@Client.on_message(filters.command("rename"))
async def rename(bot: Client, message: Message):
    user_id = message.from_user.id
    if message.reply_to_message:
        new_filename = message.text.split(" ", 1)[1].strip()  # Extract new filename from the message
        
        if not new_filename:
            await message.reply("Please provide a new filename.")
            return
        
        file = message.reply_to_message
        file_path = await bot.download_media(file)
        new_file_path = os.path.join("/tmp", new_filename)
        
        try:
            os.rename(file_path, new_file_path)
            # If thumbnail exists, embed it
            thumbnail_path = await get_thumbnail(user_id)
            thumb_dl_path = thumbnail_path if thumbnail_path else None

            await bot.send_document(
                chat_id=user_id,
                document=new_file_path,
                caption=f"Renamed file: `{new_filename}`",
                thumb=thumb_dl_path,
            )
            os.remove(new_file_path)
        except Exception as e:
            await message.reply(f"Error during renaming: {e}")
