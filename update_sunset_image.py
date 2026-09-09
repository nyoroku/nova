import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from bookings.models import Tour

# Assign new sunset image
try:
    t = Tour.objects.get(name='Sunset Cruise')
    t.image = 'tour_images/sunset_cruise_v3.png'
    t.save()
    print(f"[SUCCESS] Updated 'Sunset Cruise' to use new premium image.")
except Tour.DoesNotExist:
    print("[ERROR] 'Sunset Cruise' tour not found.")

# Verify image paths for all tours
print("\n--- Current Tour Images ---")
for t in Tour.objects.all():
    print(f"{t.name}: {t.image}")
