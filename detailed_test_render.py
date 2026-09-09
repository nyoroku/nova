import os
import django
import sys
from django.template.loader import render_to_string
from django.conf import settings

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from seo.models import LocalPage
from bookings.models import Tour

# Mock context
context = {
    'popular_locations': LocalPage.objects.filter(is_active=True),
    'featured_tours': Tour.objects.filter(is_active=True),
}

rendered = render_to_string('pages/home.html', context)

print("\n--- Checking for literal tags in Destinations ---")
if '{{ location.image.url }}' in rendered:
    print("Found literal: {{ location.image.url }}")
if '{{ location.title }}' in rendered:
    print("Found literal: {{ location.title }}")

print("\n--- Checking for literal tags in Tours ---")
if '{{ tour.image.url }}' in rendered:
    print("Found literal: {{ tour.image.url }}")
if '{{ tour.name }}' in rendered:
    print("Found literal: {{ tour.name }}")
