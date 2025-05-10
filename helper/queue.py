import asyncio
from plugins.rename import rename_file
from utils.progress import display_progress

queue = asyncio.Queue() 

async def process_queue(file_id, user_id):
    """Handles renaming requests asynchronously using a task queue."""
    
    await queue.put((file_id, user_id))  

    while not queue.empty():  
        file_id, user_id = await queue.get()

        try:
            for percent in range(0, 101, 10):
                await asyncio.sleep(1)  
                await display_progress(percent, current=percent, total=100, speed="500KB", time_remaining="5s")

            renamed_file = await rename_file(file_id, user_id)  
            
            if renamed_file:
                print(f"✅ Renaming completed successfully for file {renamed_file}")
            else:
                print(f"❌ Error: Renaming failed for file {file_id}")

        except Exception as e:
            print(f"❌ Rename error for file {file_id}: {e}")
        finally:
            queue.task_done()
