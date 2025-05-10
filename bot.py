import os
import asyncio
import threading
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from handler.start import start_bot
from plugins.rename import rename_file
from plugins.thumb import attach_thumbnail
from utils.sanitize import sanitize_filename
from utils.progress import display_progress

# Enable logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize bot with session persistence
app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, workdir="./session/")

user_states = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    logging.info("🚀 Bot received /start command.")
    await message.reply("🤖 Hello! I am Tensai Rename Bot. Send me a file to rename!")

@app.on_message(filters.photo)
async def save_thumbnail(client, message):
    try:
        file_path = await message.download()
        if not file_path:
            await message.reply("❌ Failed to save thumbnail!")
            return
        
        user_states[message.chat.id]["thumbnail"] = file_path
        await message.reply("📸 Thumbnail saved! Now send me the video file.")

    except Exception as e:
        logging.error(f"Thumbnail error: {e}")

@app.on_message(filters.video | filters.document)
async def receive_file(client, message):
    file_path = await message.download()
    user_states[message.chat.id] = {"file": file_path}
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Start Rename", callback_data="start_rename")]])
    await message.reply("📂 File received! Click below to start renaming:", reply_markup=keyboard)

@app.on_callback_query(filters.regex("start_rename"))
async def ask_for_filename(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_states[chat_id]["awaiting_rename"] = True
    await callback_query.message.reply("📝 Please send the new file name:")

@app.on_message(filters.text & filters.private)
async def rename_command(client, message):
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})
    if user_state.get("awaiting_rename"):
        new_name = sanitize_filename(message.text.strip()) + ".mp4"
        user_state["new_name"] = new_name
        user_state["awaiting_rename"] = False
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📄 Document", callback_data="output_document"),
                                          InlineKeyboardButton("🎥 Video", callback_data="output_video")]])
        await message.reply("🔰 Select Output Type:", reply_markup=keyboard)

@app.on_callback_query(filters.regex("output_document|output_video"))
async def process_rename(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_state = user_states.get(chat_id, {})
    output_type = "document" if callback_query.data == "output_document" else "video"
    user_state["output_type"] = output_type
    file_path = user_state.get("file")
    new_name = user_state.get("new_name")
    thumbnail = user_state.get("thumbnail") if output_type == "video" else None

    if not file_path or not new_name:
        await callback_query.message.reply("❌ Error: Missing file or rename input!")
        return

    await callback_query.message.reply("⚙️ Processing... Please wait.")

    try:
        new_file_path = await rename_file(file_path, new_name)
        if output_type == "video" and thumbnail:
            embedded_video = await attach_thumbnail(new_file_path, thumbnail)
            await callback_query.message.reply_video(video=embedded_video, caption="✅ Renaming Complete! Here is your renamed file.")
        else:
            await callback_query.message.reply_document(document=new_file_path, caption="✅ Renaming Complete! Here is your renamed file.")
        
        del user_states[chat_id]

    except Exception as e:
        logging.error(f"❌ Error processing file: {e}")
        await callback_query.message.reply(f"❌ Error: {e}")

async def keep_alive():
    """Periodically pings Telegram to prevent disconnection."""
    while True:
        await asyncio.sleep(30)
        logging.info("🔄 Keeping bot alive...")

# Bot startup sequence with correct log message format
if __name__ == "__main__":
    logging.info("🚀 Tensai Rename Bot is starting...")
    
    try:
        start_bot()
        threading.Thread(target=lambda: asyncio.run(keep_alive()), daemon=True).start()
        app.run()
        logging.info("🤖 Tensai Bot Started Successfully!")
    except Exception as e:
        logging.error(f"❌ Bot startup failed: {e}")
