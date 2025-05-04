import os
import time
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from helper.database import get_thumbnail
from helper.utils import progress_for_pyrogram
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RenameBot")

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except Exception as e:
        logger.error(f"❌ Error in cancel: {str(e)}")

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text("__Enter a new filename...__",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

@Client.on_callback_query(filters.regex("upload"))
async def upload_file(bot, update):
    user_id = update.from_user.id
    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1].strip()
    file = update.message.reply_to_message

    file_path = os.path.join("/tmp", new_filename)
    status = await update.message.edit("📥 Downloading to server...")
    start_time = time.time()

    try:
        downloaded_path = await bot.download_media(
            message=file,
            progress=progress_for_pyrogram,
            progress_args=("📥 Downloading...", status, start_time)
        )
    except Exception as e:
        await status.edit(f"❌ Error during download:\n{e}")
        return

    new_file_path = os.path.join("/tmp", os.path.basename(downloaded_path))
    os.rename(downloaded_path, new_file_path)

    # Extract duration if video/audio
    duration = 0
    try:
        metadata = extractMetadata(createParser(new_file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass

    # Get thumbnail path from DB
    thumbnail_path = await get_thumbnail(user_id)
    if thumbnail_path:
        thumb_dl_path = os.path.join("/tmp", f"{user_id}.jpg")
        try:
            await bot.download_media(thumbnail_path, file_name=thumb_dl_path)
        except Exception as e:
            logger.warning(f"❌ Thumbnail download failed: {e}")
            thumb_dl_path = None
    else:
        thumb_dl_path = None

    try:
        if type == "document":
            await bot.send_document(
                chat_id=user_id,
                document=new_file_path,
                caption=f"`{new_filename}`",
                thumb=thumb_dl_path if os.path.exists(thumb_dl_path or "") else None,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading document...", status, start_time)
            )
        elif type == "video":
            await bot.send_video(
                chat_id=user_id,
                video=new_file_path,
                caption=f"`{new_filename}`",
                duration=duration,
                thumb=thumb_dl_path if os.path.exists(thumb_dl_path or "") else None,
                supports_streaming=True,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading video...", status, start_time)
            )
        elif type == "audio":
            await bot.send_audio(
                chat_id=user_id,
                audio=new_file_path,
                caption=f"`{new_filename}`",
                duration=duration,
                thumb=thumb_dl_path if os.path.exists(thumb_dl_path or "") else None,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading audio...", status, start_time)
            )

        await status.delete()

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await bot.send_message(user_id, "⚠️ Retrying after flood wait...")
    except Exception as e:
        await bot.send_message(user_id, f"❌ Upload Error:\n{e}")
        return
    finally:
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        if thumb_dl_path and os.path.exists(thumb_dl_path):
            os.remove(thumb_dl_path)
