import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from handler.start import start_bot
from plugins.rename import rename_file
from plugins.thumb import attach_thumbnail
from utils.sanitize import sanitize_filename
from utils.progress import display_progress

app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Dictionary to store user states (tracking rename process)
user_states = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    """Sends welcome image along with a message when the bot starts."""
    start_image_path = "resources/start_pic.jpg"

    if os.path.exists(start_image_path):
        await message.reply_photo(photo=start_image_path, caption="🤖 Hello! I am Tensai Rename Bot.\nSend me a file to rename!")
    else:
        await message.reply("🤖 Hello! I am Tensai Rename Bot.\nSend me a file to rename!\n⚠️ Warning: Start image not found.")

@app.on_message(filters.photo)
async def save_thumbnail(client, message):
    """Stores thumbnail image and confirms receipt."""
    try:
        file_path = await message.download()
        if not file_path:
            await message.reply("❌ Error: Failed to save thumbnail!")
            return
        
        user_states[message.chat.id]["thumbnail"] = file_path
        await message.reply("📸 Thumbnail saved successfully! Now send me the video file.")

    except Exception as e:
        await message.reply(f"❌ Thumbnail processing error: {e}")

@app.on_message(filters.video | filters.document)
async def receive_file(client, message):
    """Handles file upload and prompts user to start renaming."""
    file_path = await message.download()
    user_states[message.chat.id] = {"file": file_path}

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start Rename", callback_data="start_rename")]
    ])
    
    await message.reply("📂 File received! Click below to start renaming:", reply_markup=keyboard)

@app.on_callback_query(filters.regex("start_rename"))
async def ask_for_filename(client, callback_query):
    """Asks user for filename after clicking 'Start Rename'."""
    chat_id = callback_query.message.chat.id
    user_states[chat_id]["awaiting_rename"] = True

    await callback_query.message.reply("📝 Please send the new file name:")

@app.on_message(filters.text & filters.private)
async def rename_command(client, message):
    """Captures the new filename and shows output type selection buttons."""
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})

    if user_state.get("awaiting_rename"):
        new_name = sanitize_filename(message.text.strip()) + ".mp4"
        user_state["new_name"] = new_name
        user_state["awaiting_rename"] = False

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 Document", callback_data="output_document"),
             InlineKeyboardButton("🎥 Video", callback_data="output_video")]
        ])
        
        await message.reply("🔰 Select Output Type:", reply_markup=keyboard)

@app.on_callback_query(filters.regex("output_document|output_video"))
async def process_rename(client, callback_query):
    """Executes renaming based on selected output type."""
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
        # Rename the file
        new_file_path = await rename_file(file_path, new_name)

        if not new_file_path:
            await callback_query.message.reply("❌ Rename process failed! Please try again.")
            return

        if output_type == "video" and thumbnail:
            embedded_video = await attach_thumbnail(new_file_path, thumbnail)
            
            if not embedded_video:
                await callback_query.message.reply("⚠️ Warning: Thumbnail embedding failed. Sending renamed file instead.")
                embedded_video = new_file_path

            await callback_query.message.reply_video(video=embedded_video, caption="✅ Renaming Complete! Here is your renamed file.")
        
        else:
            await callback_query.message.reply_document(document=new_file_path, caption="✅ Renaming Complete! Here is your renamed file.")

        del user_states[chat_id]  # Cleanup user state after completion

    except Exception as e:
        await callback_query.message.reply(f"❌ Error processing file: {e}")

