from pyrogram import Client, filters
import config

app = Client("TensaiBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🚀 Hello! I am Tensai Rename Bot. Send me a file to rename.")

app.run()
