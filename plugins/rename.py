import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import save_file_path
from helper.utils import sanitize_filename
from helper.queue import add_to_queue

rename_handler = Client.on_message(filters.document)

async def rename_handler(client: Client, message: Message):
    user_id = str(message.from_user.id)
    
    # Download the file
    file_name = sanitize_filename(message.document.file_name)
    temp_file_path = os.path.join("/tmp", f"{user_id}_{file_name}")
    
    await message.download(file_name=temp_file_path)
    
    # Get the thumbnail if available
    thumb_path = os.path.join("/tmp", f"{user_id}_thumb.jpg")
    if message.photo:
        await message.download(file_name=thumb_path)
    
    # Process the video: Rename and embed thumbnail
    new_file_path = os.path.join("/tmp", f"renamed_{file_name}")
    try:
        if os.path.exists(thumb_path):
            # Embedding thumbnail using FFmpeg
            (
                ffmpeg
                .input(temp_file_path)
                .output(new_file_path, vcodec="copy", acodec="copy", 
                        map="0", attach=thumb_path)
                .run(overwrite_output=True)
            )
        else:
            os.rename(temp_file_path, new_file_path)
        
        # Save file path to MongoDB
        await save_file_path(user_id, new_file_path)
        
        # Send the renamed video with thumbnail (if attached)
        await message.reply_video(video=new_file_path, caption="Here is your renamed video!")
        
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
