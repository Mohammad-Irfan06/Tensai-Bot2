import asyncio
from plugins.rename import rename_file

async def process_queue(file_id, user_id):
    await rename_file(file_id, user_id)
