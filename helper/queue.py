import asyncio
from plugins.rename import rename_file
from utils.progress import display_progress

queue = asyncio.Queue()  # Queue to handle multiple rename tasks

async def process_queue(file_id, user_id):
    """Handles renaming requests asynchronously with a queue system."""
    
    await queue.put((file_id, user_id))  # Add task to queue

    while not queue.empty():  # Process tasks one by one
        file_id, user_id = await queue.get()  # Retrieve task

        try:
            for percent in range(0, 101, 10):
                display_progress(percent, current=percent, total=100, speed='500KB', time_remaining='5s')
                await asyncio.sleep(1)  # Simulate progress updates

            await rename_file(file_id, user_id)  # Execute renaming
            print(f"✅ Renaming completed for file {file_id}")
        
        except Exception as e:
            print(f"❌ Rename error for file {file_id}: {e}")
