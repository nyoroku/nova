import os
from PIL import Image

media_dir = r"C:\Users\Administrator\PycharmProjects\boats\media\tour_images"
for filename in os.listdir(media_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(media_dir, filename)
        try:
            with Image.open(path) as img:
                img.verify()
            print(f"[OK] {filename} is a valid image. Size: {os.path.getsize(path)} bytes")
        except Exception as e:
            print(f"[ERROR] {filename} is NOT a valid image: {e}")
