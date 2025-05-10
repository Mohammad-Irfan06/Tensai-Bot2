import asyncio
import os

async def rename_file(file_path, new_name):
    await asyncio.sleep(2)  # Simulate processing
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    print(f"✔ File renamed successfully: {new_path}")
