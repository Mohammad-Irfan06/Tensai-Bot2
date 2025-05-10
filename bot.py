import os
import asyncio
from pyrogram import Client, filters
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

@app.on_message(filters.photo)  # Handles thumbnails
async def save_thumbnail(client, message):
    """Stores thumbnail image and prompts user to send a video."""
    file_path = await message.download()
    user_states[message.chat.id] = {"thumbnail": file_path}  # Store thumbnail path
    await message.reply("📸 Thumbnail saved successfully! Now send me the video file.")

@app.on_message(filters.video)  # Handles video files & starts rename process
async def receive_video(client, message):
    """Stores video and asks the user for rename input."""
    file_path = await message.download()
    user_states[message.chat.id] = {"video": file_path, "awaiting_rename": True}
    await message.reply("🎥 Video received! What should I rename it to?")

@app.on_message(filters.text & filters.private)
async def rename_command(client, message):
    """Captures the new filename and asks for the output type."""
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})

    if user_state.get("awaiting_rename"):
        new_name = sanitize_filename(message.text.strip()) + ".mp4"
        user_state["new_name"] = new_name
        user_state["awaiting_rename"] = False
        user_state["awaiting_output_type"] = True
        await message.reply("📝 Choose Output Type:\n1️⃣ Document 📄\n2️⃣ Video 🎥 (Thumbnail embedded)")

@app.on_message(filters.text & filters.private)
async def output_choice(client, message):
    """Handles output selection and executes renaming."""
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})

    if user_state.get("awaiting_output_type"):
        output_type = message.text.strip().lower()

        if output_type in ["document", "video"]:
            await message.reply("⚙️ Processing... Please wait.")
            user_state["output_type"] = output_type
            user_state["awaiting_output_type"] = False

            video_path = user_state.get("video")
            new_name = user_state.get("new_name")
            thumbnail = user_state.get("thumbnail")

            if not video_path or not new_name:
                await message.reply("❌ Error: Missing video file or rename input!")
                return

            try:
                # Display progress bar dynamically
                for percent in range(0, 101, 10):
                    await asyncio.sleep(1)
                    await display_progress(percent, current=percent, total=100, speed="500KB", time_remaining="5s", message=message)

                # Rename the file
                new_file_path = await rename_file(video_path, new_name)

                if output_type == "video" and thumbnail:
                    await attach_thumbnail(new_file_path, thumbnail)

                await message.reply(f"✅ Renaming Complete! Here is your file: `{new_file_path}`")
                del user_states[chat_id]  # Cleanup user state after completion
            except Exception as e:
                await message.reply(f"❌ Error processing file: {e}")
        else:
            await message.reply("❌ Invalid choice. Please choose **Document** or **Video**.")

if __name__ == "__main__":
    print("🚀 Tensai Rename Bot is starting...")
    start_bot()
    app.run()
