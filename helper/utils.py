import re

def sanitize_filename(filename: str) -> str:
    """Sanitize user input filename to avoid issues."""
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
