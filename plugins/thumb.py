import os
from PIL import Image
import ffmpeg

def attach_thumbnail(video_file, thumbnail_file):
    """Embeds the thumbnail into the video file safely."""

    # Ensure both files exist before proceeding
    if not os.path.exists(video_file):
        print(f"❌ Error: Video file '{video_file}' not found!")
        return
    if not os.path.exists(thumbnail_file):
        print(f"❌ Error: Thumbnail file '{thumbnail_file}' not found!")
        return

    try:
        # Resize thumbnail while preserving aspect ratio
        img = Image.open(thumbnail_file)
        img.thumbnail((300, 300))  # Auto-resize for better quality
        temp_thumb = "temp_thumbnail.jpg"
        img.save(temp_thumb)

        # Embed thumbnail into video using ffmpeg
        output_video = f"embedded_{video_file}"
        ffmpeg.input(video_file).input(temp_thumb).output(output_video, vf="thumbnail").run()

        print(f"✅ Thumbnail embedded successfully: {output_video}")
        return output_video  # Return the new file with embedded thumbnail
    except Exception as e:
        print(f"❌ Thumbnail processing error: {e}")
