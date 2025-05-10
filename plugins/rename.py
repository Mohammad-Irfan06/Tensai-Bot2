import asyncio
import os

async def rename_file(file_path, new_name):
    """Renames the given file safely with error handling and validation."""
    await asyncio.sleep(2)  # Simulate processing delay

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' does not exist!")
        return

    allowed_extensions = [".mp4", ".mkv", ".avi", ".mov"]
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in allowed_extensions:
        print(f"❌ Error: Invalid file type '{file_extension}'. Only {allowed_extensions} are allowed.")
        return

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"✔ File renamed successfully: {new_path}")
        return new_path  # Return new file path for further processing
    except Exception as e:
        print(f"❌ Rename Error: {e}")
