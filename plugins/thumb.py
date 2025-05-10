from PIL import Image

def attach_thumbnail(video_file, thumbnail_file):
    img = Image.open(thumbnail_file)
    img.thumbnail((128, 128))
    img.save(f"{video_file}_thumb.jpg")
