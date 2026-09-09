import os
from PIL import Image

def optimize_images():
    static_dir = r"c:\Users\Administrator\PycharmProjects\boats\static\images"
    hero_images = [
        "hero_local.png",
        "hero_wildlife.png",
        "hero_birds.png",
        "hero_sunset.png",
        "hero_crescent.png"
    ]

    for img_name in hero_images:
        img_path = os.path.join(static_dir, img_name)
        if not os.path.exists(img_path):
            print(f"Skipping {img_name}, not found.")
            continue

        with Image.open(img_path) as img:
            # 1. Create WebP Version (Desktop)
            webp_name = img_name.rsplit('.', 1)[0] + ".webp"
            webp_path = os.path.join(static_dir, webp_name)
            img.save(webp_path, "WEBP", quality=80)
            print(f"Created {webp_name}")

            # 2. Create Mobile Version (WebP, Max 800px width)
            mobile_webp_name = img_name.rsplit('.', 1)[0] + "_mobile.webp"
            mobile_webp_path = os.path.join(static_dir, mobile_webp_name)
            
            # Maintain aspect ratio
            w, h = img.size
            if w > 800:
                new_w = 800
                new_h = int(h * (800 / w))
                img_mobile = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                img_mobile.save(mobile_webp_path, "WEBP", quality=80)
                print(f"Created {mobile_webp_name} (Resized)")
            else:
                img.save(mobile_webp_path, "WEBP", quality=80)
                print(f"Created {mobile_webp_name} (Original size)")

if __name__ == "__main__":
    optimize_images()
