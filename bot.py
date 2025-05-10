import asyncio
from pyrogram import Client, filters
import config
from handler.start import start_bot
from plugins.rename import rename_file
from plugins.thumb import attach_thumbnail
from utils.sanitize import sanitize_filename
from utils.progress import display_progress

app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🤖 Hello! I am Tensai Rename Bot. Send me a file to rename.")

@app.on_message(filters.photo)  # Handles thumbnails
async def save_thumbnail(client, message):
    file_path = await message.download()
    await message.reply("📸 Thumbnail saved successfully! Now send me the video file.")

@app.on_message(filters.video)  # Handles video files & starts rename process
async def receive_video(client, message):
    video_path = await message.download()
    
    await message.reply(f"🎥 Video received! What should I rename it to?")
    
    # Wait for user to send a rename command
    @app.on_message(filters.text & filters.private)
    async def rename_command(client, rename_message):
        new_name = rename_message.text.strip() + ".mp4"
        await message.reply("📝 Choose Output Type:\n1️⃣ Document 📄\n2️⃣ Video 🎥 (Thumbnail embedded)")
        
        # Wait for user choice
        @app.on_message(filters.text & filters.private)
        async def output_choice(client, choice_message):
            output_type = choice_message.text.strip().lower()
            
            if output_type in ["document", "video"]:
                await message.reply("⚙️ Processing... Please wait.")

                # Show Progress Bar
                for percent in range(0, 101, 10):
                    display_progress(percent, current=percent, total=100, speed='500KB', time_remaining='5s')

                # Rename the file
                await rename_file(video_path, new_name)

                if output_type == "video":
                    await attach_thumbnail(new_name, "thumbnail.jpg")  # Embed thumbnail

                await message.reply(f"✅ Renaming Complete! Here is your file: `{new_name}`")
            else:
                await message.reply("❌ Invalid choice. Please choose **Document** or **Video**.")
