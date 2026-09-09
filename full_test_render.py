import os
import django
import sys
from django.template.loader import render_to_string
from django.conf import settings

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from seo.models import LocalPage
from services.models import Service
from bookings.models import Tour

# Mock context
context = {
    'popular_locations': LocalPage.objects.filter(is_active=True),
    'services': Service.objects.filter(is_active=True),
    'featured_tours': Tour.objects.filter(is_active=True),
}

try:
    rendered = render_to_string('pages/home.html', context)
    print("SUCCESS: Template rendered correctly.")
    # Check for literal tags in the output
    if '{{' in rendered or '{%' in rendered:
        print("WARNING: Literal tags found in rendered output!")
        # Print a few lines around the literal tag
        idx = rendered.find('{{')
        if idx == -1: idx = rendered.find('{%')
        print(f"Sample around literal tag: {rendered[max(0, idx-50):min(len(rendered), idx+100)]}")
    else:
        print("NO literal tags found in rendered output.")
except Exception as e:
    print(f"FAILED to render template: {e}")
