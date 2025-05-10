import re

def sanitize_filename(filename: str) -> str:
    """Sanitizes user input filename to avoid invalid characters while keeping useful ones."""
    
    if not filename or not isinstance(filename, str) or len(filename.strip()) == 0:
        print("❌ Error: Invalid filename input!")
        return None  
    
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\. ()]', '_', filename.strip())
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    sanitized = sanitized.strip('.')

    allowed_extensions = {".mp4", ".mkv", ".avi", ".mov"}
    file_extension = f".{sanitized.split('.')[-1]}" if '.' in sanitized else ""

    if file_extension not in allowed_extensions:
        sanitized += ".mp4"  
    
    return sanitized
