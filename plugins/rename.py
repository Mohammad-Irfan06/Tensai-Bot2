import os
import asyncio
import subprocess
from pyrogram.types import Message
from thumb import attach_thumbnail

async def rename_file(file_path, new_name):
    """Safely renames a file with error handling."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found!")
        return None

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"✅ File renamed successfully: {new_path}")
        return new_path  
    except Exception as e:
        print(f"❌ Rename Error: {e}")
        return None

async def embed_thumbnail(input_file, output_file, thumbnail_file):
    """Embeds thumbnail into a video using ffmpeg."""
    try:
        # Log paths and files
        print(f"DEBUG: Embedding thumbnail for {input_file} with {thumbnail_file}")
        
        # FFmpeg command to embed thumbnail
        cmd = [
            "ffmpeg", "-i", input_file, "-i", thumbnail_file,
            "-map", "0", "-map", "1", "-c", "copy",
            "-disposition:1", "attached_pic", output_file
        ]
        print(f"DEBUG: Running command: {' '.join(cmd)}")  # Log the ffmpeg command
        subprocess.run(cmd, check=True)
        print("✅ Thumbnail embedded successfully")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error: {e}")
        return input_file  # fallback to original if error
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return input_file

async def send_output_file(bot, message: Message, output_path, thumb_path=None, as_video=False, caption=""):
    """Sends the output file either as video or document."""

    # If video is sent, use the thumbnail
    if as_video and output_path.lower().endswith(('.mp4', '.mkv', '.webm')):
        try:
            # Check if thumbnail exists
            if thumb_path:
                print(f"DEBUG: Thumbnail path: {thumb_path}")
            else:
                print("DEBUG: No thumbnail provided")

            # Send video with thumbnail
            await message.reply_video(
                video=output_path,
                caption=caption,
                thumb=thumb_path if thumb_path and os.path.exists(thumb_path) else None,
                supports_streaming=True
            )
            print("✅ Video sent with thumbnail")
        except Exception as e:
            print(f"❌ send_video failed: {e}")
            await message.reply_document(document=output_path, caption=caption)
    else:
        await message.reply_document(document=output_path, caption=caption)
        print("📁 Sent as document (fallback)")
