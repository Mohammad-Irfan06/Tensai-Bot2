import os
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.photo)
async def thumb_handler(client: Client, message: Message):
    user_id = str(message.from_user.id)
    
    # Save the thumbnail sent by the user
    thumb_path = os.path.join("downloads", f"{user_id}.jpg")
    
    # Download the thumbnail image
    await message.download(file_name=thumb_path)
    
    # Confirm that the thumbnail is saved
    await message.reply_text("Thumbnail saved successfully!")
