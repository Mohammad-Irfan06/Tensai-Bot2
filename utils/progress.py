import asyncio

async def display_progress(percent, current, total, speed, time_remaining, message):
    """Displays progress dynamically in Telegram bot messages."""
    progress_bar = "⭐" * (percent // 10) + "☆" * (10 - percent // 10)
    progress_text = f"""
🤖 Tensai Processing: [{progress_bar}] {percent}%
╭━━━━❰ Processing Video ❱━➣
┣⪼ 🗂️ : {current}/{total} | {percent}%
┣⪼ ⏳️ Estimated Time Remaining: {time_remaining}
┣⪼ 🚀 Speed: {speed}/s
╰━━━━━━━━━━━━━━━➣
"""

    await message.edit(progress_text)  # Send updates directly to Telegram
    await asyncio.sleep(1)  # Ensures non-blocking execution
