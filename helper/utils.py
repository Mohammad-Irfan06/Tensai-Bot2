from pyrogram.types import Message
import time

def progress_for_pyrogram(current, total, message: Message, start_time: float, prefix=""):
    """
    This function displays the progress of file download or upload in Pyrogram.
    current: Current size of the file being transferred
    total: Total size of the file
    message: The message to update the progress in
    start_time: Time when the transfer started
    prefix: Optional message prefix (e.g., "Downloading...", "Uploading...")
    """
    elapsed_time = time.time() - start_time
    if total > 0:
        percent = (current / total) * 100
        speed = current / elapsed_time if elapsed_time > 0 else 0
        remaining_time = (total - current) / speed if speed > 0 else 0

        progress = f"{prefix} [{percent:.2f}%] {current}/{total} bytes @ {speed:.2f} B/s remaining {remaining_time:.2f}s"
        message.edit(progress)
