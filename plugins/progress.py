import time

class ProgressBar:
    @staticmethod
    def send_progress(current, total, message, client):
        # Calculate the percentage progress
        percent = (current / total) * 100
        
        # Speed calculation (downloaded so far / time elapsed)
        if not hasattr(message, 'start_time'):  # If it's the first time, initialize the start time
            message.start_time = time.time()  # Store start time to calculate elapsed time

        elapsed_time = time.time() - message.start_time  # Calculate elapsed time in seconds
        speed = current / elapsed_time if elapsed_time > 0 else 0  # Calculate download speed
        
        # Estimate the time remaining (total - current) / speed
        time_remaining = (total - current) / speed if speed > 0 else 0
        time_remaining = int(time_remaining)

        # Construct the progress message using the formatted string
        progress_message = """\n
🤖 Tensai Processing: [⭐⭐⭐⭐⭐⭐⭐☆☆☆☆☆☆☆☆☆] {0:.2f}%
╭━━━━❰ Tensai Hacking... ❱━➣
┣⪼ 🗂️ : {1}/{2} | {0:.2f}%
┣⪼ ⏳️ : {0:.2f}%
┣⪼ 🚀 : {3:.2f} KB/s
┣⪼ ⏱️ : {4}s
╰━━━━━━━━━━━━━━━➣""".format(percent, current, total, speed / 1024, time_remaining)  # Dividing speed by 1024 for KB/s

        # Send or update the progress message to the user
        client.edit_message_text(message.chat.id, message.message_id, progress_message)
