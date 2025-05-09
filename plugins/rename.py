import os
import ffmpeg
from pyrogram import Client
from pyrogram.types import Message
from config import DOWNLOAD_DIR
from helper.utils import sanitize_filename
from plugins.progress import ProgressBar

async def rename_handler(client: Client, message: Message):
    user_id = str(message.from_user.id)

    # Download path
    temp_file_path = os.path.join(DOWNLOAD_DIR, f"{user_id}_raw.mp4")

    # Initialize progress message
    progress_msg = await message.reply_text("Downloading file...")

    # Download the file with progress
    await message.download(file_name=temp_file_path, progress=ProgressBar.send_progress, progress_args=(client, progress_msg))

    # After download, rename and process video
    file_name = sanitize_filename(message.document.file_name)
    new_file_path = os.path.join(DOWNLOAD_DIR, f"renamed_{file_name}")

    thumb_path = os.path.join(DOWNLOAD_DIR, f"{user_id}.jpg")

    # Handle the thumbnail if available
    try:
        if os.path.exists(thumb_path):
            # Embed the thumbnail using FFmpeg
            (
                ffmpeg
                .input(temp_file_path)
                .output(new_file_path, vcodec="copy", acodec="copy", 
                        map="0", attach=thumb_path)
                .run(overwrite_output=True)
            )
        else:
            os.rename(temp_file_path, new_file_path)

        # Send the renamed video with progress updates
        await message.reply_video(video=new_file_path, caption="Here is your renamed video with thumbnail!")

        # Update the progress message once done
        await progress_msg.edit_text("Renaming completed!")

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        await progress_msg.edit_text(f"Error: {e}")
