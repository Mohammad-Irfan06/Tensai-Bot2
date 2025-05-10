import asyncio 
from pyrogram import Client, filters
import config

app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🚀 Hello! I am Tensai Rename Bot. Send me a file to rename.")

@app.on_message(filters.photo)  # Handles thumbnails
async def save_thumbnail(client, message):
    await message.photo.download("thumbnail.jpg")
    await message.reply("📸 Thumbnail saved successfully!")

@app.on_message(filters.video)  # Handles video files
async def receive_video(client, message):
    video_path = await message.video.download()
    await message.reply("🎥 Video received! What should I rename it to?")

from pyrogram import idle

async def main():
    start_bot()
    print("Bot is running and listening for events...")
    await idle()  # Keeps the bot running

if __name__ == "__main__":
    asyncio.run(main())
