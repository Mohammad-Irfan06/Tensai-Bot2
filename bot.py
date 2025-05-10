import asyncio
from pyrogram import Client, filters
import config
from handler.start import start_bot

# Initialize Bot Client
app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🚀 Hello! I am Tensai Rename Bot. Send me a file to rename.")

@app.on_message(filters.photo)  # Handles thumbnails
async def save_thumbnail(client, message):
    file_path = await message.download()  # Correct method to download the file
    await message.reply("📸 Thumbnail saved successfully!")
    print(f"Thumbnail saved at {file_path}")  # Debugging log

@app.on_message(filters.video)  # Handles video files
async def receive_video(client, message):
    video_path = await message.video.download()
    await message.reply("🎥 Video received! What should I rename it to?")

# Start Bot Function
def main():
    start_bot()
    print("Bot is running and listening for events...")
    app.run()  # Pyrogram handles its own event loop, no need for asyncio.run()

if __name__ == "__main__":
    main()
