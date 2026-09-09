import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from bookings.models import Tour
from django.conf import settings

t = Tour.objects.first()
print(f"DEBUG: {settings.DEBUG}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
if t and t.image:
    print(f"Tour Name: {t.name}")
    print(f"Image Field: {t.image}")
    print(f"Image URL: {t.image.url}")
    print(f"Full Path: {os.path.join(settings.MEDIA_ROOT, str(t.image))}")
    print(f"File Exists: {os.path.exists(os.path.join(settings.MEDIA_ROOT, str(t.image)))}")
else:
    print("No tour or no image.")
