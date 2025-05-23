import os
import ffmpeg
from PIL import Image

def attach_thumbnail(video_file, thumbnail_file):
    """Embeds the thumbnail into a video file as metadata thumbnail."""

    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return None

    if not os.path.exists(thumbnail_file):
        print(f"❌ Thumbnail file not found: {thumbnail_file}")
        return None

    try:
        # Convert thumbnail to jpg and resize
        img = Image.open(thumbnail_file)
        img.thumbnail((320, 320))  # Safe Telegram size
        temp_thumb = "temp_thumbnail.jpg"
        img.save(temp_thumb, "JPEG", quality=85)
        print(f"✅ Thumbnail converted and saved as {temp_thumb}")

        output_path = f"embedded_{os.path.basename(video_file)}"

        # Use ffmpeg to embed the thumbnail into the video
        print(f"DEBUG: Embedding thumbnail into {video_file}...")
        ffmpeg.input(video_file).output(output_path, map='0:v:0', map='1:v:0', c='copy', dis='1', i=temp_thumb).run()

        # Cleanup the temporary thumbnail file
        os.remove(temp_thumb)
        print(f"✅ Temporary thumbnail removed: {temp_thumb}")

        print(f"✅ Thumbnail embedded successfully into {output_path}")
        return output_path

    except ffmpeg.Error as e:
        print(f"❌ FFmpeg error: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
