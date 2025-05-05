from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

callback_handler = Client.on_callback_query(filters.regex(".*"))

async def callback_handler(client: Client, callback_query: CallbackQuery):
    await callback_query.answer("Processing...")
