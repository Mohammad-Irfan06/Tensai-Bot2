import asyncio
import os

async def rename_file(file_path, new_name):
    """Safely renames a file with error handling and validation."""
    await asyncio.sleep(2)  

    if not os.path.exists(file_path):
        return None

    if not new_name or not isinstance(new_name, str) or len(new_name.strip()) == 0:
        return None

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        return new_path  
    except Exception as e:
        return None
