import os
import subprocess
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

        output_path = f"embedded_{os.path.basename(video_file)}"

        # FFmpeg command to embed thumbnail
        cmd = [
            "ffmpeg", "-i", video_file, "-i", temp_thumb,
            "-map", "0", "-map", "1", "-c", "copy",
            "-disposition:1", "attached_pic", output_path
        ]
        print(f"✅ Running FFmpeg Command: {' '.join(cmd)}")

        # Run the FFmpeg command and capture output for debugging
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Check if the FFmpeg command ran successfully
        if result.returncode == 0:
            print(f"✅ Thumbnail embedded successfully into {output_path}")
        else:
            print(f"❌ FFmpeg failed with error code {result.returncode}")
            print(f"FFmpeg Error: {result.stderr}")

        # Cleanup the temporary thumbnail file
        os.remove(temp_thumb)

        return output_path

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    finally:
        # Ensure temporary thumbnail cleanup even in case of error
        if os.path.exists(temp_thumb):
            os.remove(temp_thumb)
