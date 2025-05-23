import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from plugins.thumb import attach_thumbnail

app = Client("ThumbnailEmbedBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Dictionary to store user states (tracking files)
user_states = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    """Welcome message."""
    await message.reply("🤖 Hello! Send me a video and a thumbnail to embed the thumbnail into the video.")

@app.on_message(filters.photo)
async def save_thumbnail(client, message):
    """Store thumbnail image."""
    try:
        file_path = await message.download()
        user_states[message.chat.id] = {"thumbnail": file_path}
        await message.reply("📸 Thumbnail saved! Now, send me the video file.")
    except Exception as e:
        print(f"❌ Thumbnail download failed: {e}")

@app.on_message(filters.video)
async def receive_video(client, message):
    """Store video and ask user to start renaming."""
    try:
        file_path = await message.download()
        user_states[message.chat.id]["file"] = file_path

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Embed Thumbnail", callback_data="embed_thumbnail")]
        ])
        
        await message.reply("📂 Video received! Click below to embed the thumbnail:", reply_markup=keyboard)
    except Exception as e:
        print(f"❌ Video download failed: {e}")

@app.on_callback_query(filters.regex("embed_thumbnail"))
async def embed_thumbnail(client, callback_query):
    """Embed the thumbnail and send the video back."""
    chat_id = callback_query.message.chat.id
    user_state = user_states.get(chat_id, {})

    video_path = user_state.get("file")
    thumbnail_path = user_state.get("thumbnail")

    if not video_path or not thumbnail_path:
        await callback_query.message.reply("❌ Error: Missing video or thumbnail.")
        return

    try:
        # Embed the thumbnail into the video asynchronously
        final_video = await asyncio.to_thread(attach_thumbnail, video_path, thumbnail_path)
        if final_video:
            await client.send_video(
                chat_id=chat_id,
                video=final_video,
                caption="✅ Video with embedded thumbnail!"
            )
        else:
            await callback_query.message.reply("❌ Error: Thumbnail embedding failed.")
    except Exception as e:
        await callback_query.message.reply(f"❌ Error: {e}")

if __name__ == "__main__":
    app.run()
