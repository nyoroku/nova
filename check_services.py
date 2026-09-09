import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from services.models import Service

print(f"Total Services: {Service.objects.count()}")
for s in Service.objects.all():
    print(f"- {s.title}: Image={s.image}")
