import asyncio
import os

async def rename_file(file_path, new_name):
    """Safely renames a file with error handling and validation."""
    await asyncio.sleep(2)  

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' does not exist!")
        return None

    if not new_name or not isinstance(new_name, str) or len(new_name.strip()) == 0:
        print(f"❌ Error: Invalid new file name!")
        return None

    allowed_extensions = [".mp4", ".mkv", ".avi", ".mov"]
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in allowed_extensions:
        print(f"❌ Error: Unsupported file type '{file_extension}'. Allowed: {allowed_extensions}")
        return None

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"✅ File renamed successfully: {new_path}")
        return new_path  
    except Exception as e:
        print(f"❌ Rename Error: {e}")
        return None
