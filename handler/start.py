from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(bot, message):
    user_id = message.from_user.id
    welcome_text = f"Hello, {message.from_user.first_name}!\n\nWelcome to the Telegram Rename Bot. \nUse the bot to rename your files and add custom thumbnails. Just send a file and follow the prompts."
    
    await message.reply_text(welcome_text)
