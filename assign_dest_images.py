import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from seo.models import LocalPage

# Map titles to images
mapping = {
    'Boat Rides Naivasha': 'location_images/boat_rides.png',
    'Crescent Island Tours': 'location_images/crescent_island.png',
    'Sunset Cruises Naivasha': 'location_images/sunset_cruise.png',
}

print("Assigning images to Destinations...")
for title, img_path in mapping.items():
    try:
        lp = LocalPage.objects.get(title=title)
        lp.image = img_path
        lp.save()
        print(f"[SUCCESS] Assigned {img_path} to '{title}'")
    except LocalPage.DoesNotExist:
        print(f"[WARNING] Destination '{title}' not found!")

print("Done.")
