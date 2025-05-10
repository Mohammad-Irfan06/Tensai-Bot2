import os
import asyncio

async def rename_file(file_path, new_name):
    """Safely renames a file with error handling."""
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found!")
        return None

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"✅ File renamed successfully: {new_path}")
        return new_path  
    except Exception as e:
        print(f"❌ Rename Error: {e}")
        return None
