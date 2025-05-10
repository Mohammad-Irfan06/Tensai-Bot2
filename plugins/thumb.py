import os
from PIL import Image
import ffmpeg

def attach_thumbnail(video_file, thumbnail_file):
    """Embeds the thumbnail into a video safely with error handling."""
    
    if not os.path.exists(video_file) or not os.path.exists(thumbnail_file):
        return None

    try:
        img = Image.open(thumbnail_file)
        img.thumbnail((400, 400), Image.ANTIALIAS)  
        temp_thumb = "temp_thumbnail.jpg"
        img.save(temp_thumb, "JPEG", quality=85) 
        
        output_video = f"embedded_{os.path.basename(video_file)}"
        ffmpeg.input(video_file).input(temp_thumb).output(output_video, vcodec="libx264", movflags="faststart").run()

        return output_video  
    
    except Exception as e:
        return None
