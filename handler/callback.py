import asyncio
from helper.queue import process_queue
from utils.progress import display_progress

async def handle_callback(data):
    """Handles file processing requests with error handling."""
    file_id = data.get('file_id')  
    user_id = data.get('user_id')

    if not file_id or not user_id:
        print("⚠️ Error: Missing file_id or user_id in request.")
        return

    print(f"🔄 Processing rename request for User: {user_id}, File: {file_id}")

    try:
        await process_queue(file_id, user_id, display_progress)
        print(f"✅ Rename process completed successfully for User: {user_id}")
    except Exception as e:
        print(f"❌ Error during rename process for User {user_id}: {e}")
