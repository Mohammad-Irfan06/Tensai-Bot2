import os
from PIL import Image
import ffmpeg

def attach_thumbnail(video_file, thumbnail_file):
    """Embeds the thumbnail into a video safely with error handling."""
    
    if not os.path.exists(video_file) or not os.path.exists(thumbnail_file):
        print(f"❌ Error: Video or thumbnail file not found!")
        return None

    try:
        img = Image.open(thumbnail_file)
        img.thumbnail((400, 400))
        temp_thumb = "temp_thumbnail.jpg"
        img.save(temp_thumb, "JPEG", quality=85) 
        
        output_video = f"embedded_{os.path.basename(video_file)}"
        
        process = (
            ffmpeg.input(video_file)
            .input(temp_thumb, loop=1)
            .output(output_video, vcodec="libx264", movflags="faststart", pix_fmt="yuv420p")
            .run(capture_stdout=True, capture_stderr=True)
        )

        print(f"✅ Thumbnail successfully embedded: {output_video}")
        return output_video  

    except Exception as e:
        print(f"❌ Unexpected Thumbnail Error: {e}")
        return None
