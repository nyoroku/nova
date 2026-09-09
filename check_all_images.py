import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from bookings.models import Tour
from services.models import Service
from seo.models import LocalPage
from django.conf import settings

def check_model(model_class, name_field, img_field='image'):
    print(f"\n--- Checking {model_class.__name__} ---")
    for obj in model_class.objects.all():
        img = getattr(obj, img_field)
        name = getattr(obj, name_field)
        if img:
            full_path = os.path.join(settings.MEDIA_ROOT, str(img))
            exists = os.path.exists(full_path)
            print(f"[{'OK' if exists else 'MISSING'}] {name} -> {img.url}")
        else:
            print(f"[EMPTY] {name}")

check_model(Service, 'title')
check_model(LocalPage, 'title')
check_model(Tour, 'name')
