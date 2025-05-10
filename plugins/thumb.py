import os
import logging
from PIL import Image
import ffmpeg

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def attach_thumbnail(video_file, thumbnail_file):
    if not os.path.exists(video_file) or not os.path.exists(thumbnail_file):
        logging.error("❌ Video or thumbnail file missing!")
        return None

    try:
        img = Image.open(thumbnail_file)
        img.thumbnail((400, 400))
        temp_thumb = "temp_thumbnail.jpg"
        img.save(temp_thumb, "JPEG", quality=85)
        output_video = f"embedded_{os.path.basename(video_file)}"
        ffmpeg.input(video_file).input(temp_thumb, loop=1).output(output_video, vcodec="libx264", movflags="faststart", pix_fmt="yuv420p").run()
        logging.info(f"✅ Thumbnail embedded successfully: {output_video}")
        return output_video  

    except Exception as e:
        logging.error(f"❌ FFmpeg Error: {e}")
        return None
