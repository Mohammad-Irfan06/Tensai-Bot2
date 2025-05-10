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
    await message.reply("🤖 Hello! I am Tensai Rename Bot. Send me a file to rename.")

@app.on_message(filters.photo)  # Handles thumbnails
async def save_thumbnail(client, message):
    file_path = await message.download()
    await message.reply("📸 Thumbnail saved successfully! Now send me the video file.")
    user_states[message.chat.id] = {"thumbnail": file_path}  # Store thumbnail path

@app.on_message(filters.video)  # Handles video files & starts rename process
async def receive_video(client, message):
    video_path = await message.download()
    user_states[message.chat.id] = {"video": video_path}
    
    await message.reply(f"🎥 Video received! What should I rename it to?")
    user_states[message.chat.id]["awaiting_rename"] = True  # Track rename state

@app.on_message(filters.text & filters.private)
async def rename_command(client, message):
    chat_id = message.chat.id

    if user_states.get(chat_id, {}).get("awaiting_rename"):
        new_name = sanitize_filename(message.text.strip()) + ".mp4"
        user_states[chat_id]["new_name"] = new_name
        user_states[chat_id]["awaiting_rename"] = False  # Rename process confirmed
        
        await message.reply("📝 Choose Output Type:\n1️⃣ Document 📄\n2️⃣ Video 🎥 (Thumbnail embedded)")
        user_states[chat_id]["awaiting_output_type"] = True  # Track output type selection

@app.on_message(filters.text & filters.private)
async def output_choice(client, message):
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})

    if user_state.get("awaiting_output_type"):
        output_type = message.text.strip().lower()
        
        if output_type in ["document", "video"]:
            await message.reply("⚙️ Processing... Please wait.")
            user_state["output_type"] = output_type
            user_state["awaiting_output_type"] = False  # Confirm output type
            
            video_path = user_state.get("video")
            new_name = user_state.get("new_name")
            thumbnail = user_state.get("thumbnail")

            if not video_path or not new_name:
                await message.reply("❌ Error: Missing video file or rename input!")
                return

            # Show Progress Bar
            for percent in range(0, 101, 10):
                await asyncio.sleep(1)  # Non-blocking execution
                await display_progress(percent, current=percent, total=100, speed='500KB', time_remaining='5s', message=message)

            # Rename the file
            try:
                new_file_path = await rename_file(video_path, new_name)
                if output_type == "video" and thumbnail:
                    await attach_thumbnail(new_file_path, thumbnail)  # Embed thumbnail

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
