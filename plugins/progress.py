async def send_progress(client, message, current, total):
    """
    This function sends the progress of the download or upload process.
    It calculates the percentage and updates the message with progress details.
    """
    percent = (current / total) * 100
    progress_bar = "⭐" * int(percent // 10) + "☆" * (10 - int(percent // 10))
    progress_text = f"🤖 Tensai Processing: [{progress_bar}] {percent:.2f}%\n"
    
    # Send a progress update
    await message.edit_text(progress_text



class mr(object):
    PROGRESS_BAR = """\n
🤖 Tensai Processing: [⭐⭐⭐⭐⭐⭐⭐☆☆☆☆☆☆☆☆☆] {0}%
╭━━━━❰ Tensai Hacking... ❱━➣
┣⪼ 🗂️ : {1}/{2} | {0}%
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣"""
