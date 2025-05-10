import re

def sanitize_filename(filename: str) -> str:
    """Sanitizes user input filename to avoid issues while keeping useful characters."""
    # Allow letters, numbers, underscore, dash, dot, space, and parentheses
    sanitized = re.sub(r'[^a-zA-Z0-9_\-\. ()]', '_', filename)

    # Replace multiple underscores with a single underscore
    sanitized = re.sub(r'_{2,}', '_', sanitized)

    # Ensure filename does not start or end with a dot (invalid names)
    sanitized = sanitized.strip('.')

    # Limit file extensions to safe formats
    allowed_extensions = {".mp4", ".mkv", ".avi", ".mov", ".pdf", ".docx", ".jpg", ".png"}
    file_extension = f".{sanitized.split('.')[-1]}" if '.' in sanitized else ""

    if file_extension not in allowed_extensions:
        print(f"❌ Warning: Invalid file extension '{file_extension}'. Allowed formats: {allowed_extensions}")
        sanitized += ".mp4"  # Default to mp4 if no valid extension found
    
    return sanitized
