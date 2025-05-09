from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query()
async def handle_callbacks(bot, query):
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
        # Back to home logic, if needed
        await query.message.reply_text(
            "Welcome to Tensai Bot! Send me a file to rename.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Help", callback_data="how_to_use")],
                [InlineKeyboardButton("About", callback_data="about")]
            ])
        )
