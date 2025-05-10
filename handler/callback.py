from helper.queue import process_queue
from utils.progress import display_progress

async def handle_callback(data):
    file_id = data.get('file_id')  # Avoids KeyError
    user_id = data.get('user_id')

    if not file_id or not user_id:
        print("⚠️ Error: Missing file_id or user_id in request.")
        return

    print(f"🔄 Processing rename for User: {user_id}, File: {file_id}")

    # Start processing and show progress dynamically
    await process_queue(file_id, user_id, display_progress)
