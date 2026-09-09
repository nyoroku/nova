import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from seo.models import LocalPage

print(f"Total LocalPages: {LocalPage.objects.count()}")
for lp in LocalPage.objects.all():
    print(f"- {lp.title}: Image={lp.image}")
