import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def rename_file(file_path, new_name):
    if not os.path.exists(file_path):
        logging.error(f"❌ Error: File '{file_path}' not found!")
        return None

    try:
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        logging.info(f"✅ File renamed successfully: {new_path}")
        return new_path  
    except Exception as e:
        logging.error(f"❌ Rename Error: {e}")
        return None
