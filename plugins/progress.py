import time

def track_progress():
    for percent in range(0, 101, 10):
        time.sleep(1)
        print(f"Processing... {percent}% Done!")

def display_progress(percent, current, total, speed, time_remaining):
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
