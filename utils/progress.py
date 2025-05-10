def display_progress(percent, current, total, speed, time_remaining):
    """Displays progress visually."""
    progress_bar = "⭐" * (percent // 10) + "☆" * (10 - percent // 10)
    print(f"""
🤖 Tensai Processing: [{progress_bar}] {percent}%
╭━━━━❰ Tensai Hacking... ❱━➣
┣⪼ 🗂️ : {current}/{total} | {percent}%
┣⪼ ⏳️ : {percent}%
┣⪼ 🚀 : {speed}/s
┣⪼ ⏱️ : {time_remaining}
╰━━━━━━━━━━━━━━━➣
""")
