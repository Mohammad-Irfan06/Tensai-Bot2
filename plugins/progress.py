class ProgressBar:
    @staticmethod
    def send_progress(current, total, message, client):
        # Calculate the percentage progress
        percent = (current / total) * 100
        # Example for calculating the speed and time remaining
        speed = current / 1  # This is a placeholder. Implement actual speed calculation logic.
        time_remaining = (total - current) / speed  # Basic time estimation
        
        # Construct the progress message using the formatted string
        progress_message = """\n
🤖 Tensai Processing: [⭐⭐⭐⭐⭐⭐⭐☆☆☆☆☆☆☆☆☆] {0}%
╭━━━━❰ Tensai Hacking... ❱━➣
┣⪼ 🗂️ : {1}/{2} | {0}%
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣""".format(percent, current, total, speed, time_remaining)
        
        # Send or update the progress message to the user
        client.edit_message_text(message.chat.id, message.message_id, progress_message)
