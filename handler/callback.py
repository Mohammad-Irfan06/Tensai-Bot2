from helper.queue import process_queue
from utils.progress import display_progress

async def handle_callback(data):
    file_id = data['file_id']
    user_id = data['user_id']

    # Show progress while renaming
    for percent in range(0, 101, 10):
        display_progress(percent, current=percent, total=100, speed='500KB', time_remaining='5s')

    await process_queue(file_id, user_id)
