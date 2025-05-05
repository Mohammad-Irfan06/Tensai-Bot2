import asyncio
from asyncio import Queue

file_queue = Queue()

async def process_file_queue():
    while True:
        file_data = await file_queue.get()
        # Process file (e.g., renaming and thumbnail embedding)
        await process_file(file_data)
        file_queue.task_done()

async def add_to_queue(file_data):
    await file_queue.put(file_data)
