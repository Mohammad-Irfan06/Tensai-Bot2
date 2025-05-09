from pyrogram import Client
from pyrogram.types import CallbackQuery

async def callback_handler(client: Client, callback_query: CallbackQuery):
    # Handle callback query from inline buttons (if any)
    await callback_query.answer("Callback received!")
