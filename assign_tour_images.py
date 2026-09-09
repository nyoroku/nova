import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from bookings.models import Tour

# Map tour names to images
mapping = {
    'Crescent Island Walking Safari': 'tour_images/crescent_walking.png',
    'Full Day Lake Adventure': 'tour_images/full_day.png',
    'Hippo & Bird Safari': 'tour_images/hippo_bird.png',
    'Photography Safari': 'tour_images/photography.png',
    'Private Charter': 'tour_images/private_charter.png',
    'Sunset Cruise': 'tour_images/sunset_cruise.png',
}

print("Assigning images to Tours...")
for name, img_path in mapping.items():
    try:
        t = Tour.objects.get(name=name)
        t.image = img_path
        t.save()
        print(f"[SUCCESS] Assigned {img_path} to '{name}'")
    except Tour.DoesNotExist:
        print(f"[WARNING] Tour '{name}' not found!")

print("Done.")
