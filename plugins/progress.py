import os
from pyrogram import Client
from pyrogram.types import Message

# Function to handle progress
def progress(current, total):
    percentage = (current / total) * 100
    return f"Processing: {current}/{total} bytes ({percentage:.2f}%)"

# Progress handler
async def send_progress(client: Client, message: Message, current: int, total: int):
    progress_message = progress(current, total)
    await message.edit_text(progress_message)

