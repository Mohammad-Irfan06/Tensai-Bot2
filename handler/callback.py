from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handler.start import start

@Client.on_callback_query()
async def handle_callbacks(bot, query):
    try:
        if query.data == "how_to_use":
            await query.message.edit_text(
                "**📋 How to Use Tensai Bot:**\n\n"
                "1. Send me any file.\n"
                "2. I’ll ask you for a new filename.\n"
                "3. I’ll rename and send the file back with a thumbnail (if set).\n"
                "4. You can also change your custom thumbnail anytime.\n",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]])
            )

        elif query.data == "about":
            await query.message.edit_text(
                "**ℹ️ About Tensai Bot**\n\n"
                "⚡ Powered by Pyrogram & Python\n"
                "📁 Supports All File Types\n"
                "🎨 Thumbnail + Progress\n"
                "👨‍💻 Developer: @YourUsername\n",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]])
            )

        elif query.data == "back_to_home":
            await start(bot, query.message)  # Ensure start() handles exceptions properly

    except Exception as e:
        logger.error(f"Callback handler error: {e}")
        await query.message.edit_text("An error occurred, please try again later.")
