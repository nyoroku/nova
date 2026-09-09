import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from bookings.models import Tour

print(f"Total Tours: {Tour.objects.count()}")
for t in Tour.objects.all():
    print(f"- {t.name}: Image={t.image}")
