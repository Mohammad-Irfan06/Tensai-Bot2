import asyncio

async def display_progress(percent, current, total, speed, time_remaining, message):
    """Displays progress dynamically in Telegram bot messages with error handling."""
    
    if not message:
        print("⚠️ Error: Message object missing in progress update!")
        return

    progress_bar = "⭐" * (percent // 10) + "☆" * (10 - percent // 10)
    progress_text = f"""
🤖 Tensai Processing: [{progress_bar}] {percent}%
╭━━━━❰ Processing Video ❱━➣
┣⪼ 🗂️ : {current}/{total} | {percent}%
┣⪼ ⏳️ Estimated Time Remaining: {time_remaining}
┣⪼ 🚀 Speed: {speed}/s
╰━━━━━━━━━━━━━━━➣
"""

    try:
        await message.edit(progress_text)  
        await asyncio.sleep(1)  
    except Exception as e:
        print(f"❌ Error updating progress: {e}")
