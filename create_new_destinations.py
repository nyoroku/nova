import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from seo.models import LocalPage

new_pages = [
    {
        'title': 'Hippo Point Naivasha',
        'location': 'Lake Naivasha',
        'image': 'location_images/hippo_point.png',
        'primary_keyword': 'Hippo Point boat rides',
        'content': '<p>Experience the spectacular Hippo Point, home to hundreds of hippos and diverse bird species.</p>'
    },
    {
        'title': 'Elsamere Conservation Centre',
        'location': 'Southern Shore, Naivasha',
        'image': 'location_images/elsamere.png',
        'primary_keyword': 'Elsamere boat tour',
        'content': '<p>Visit the historic home of Joy Adamson and support conservation while enjoying the serene lake views.</p>'
    }
]

print("Creating new LocalPage destinations...")
for data in new_pages:
    lp, created = LocalPage.objects.get_or_create(
        title=data['title'],
        defaults={
            'location': data['location'],
            'image': data['image'],
            'primary_keyword': data['primary_keyword'],
            'content': data['content'],
            'is_active': True
        }
    )
    if created:
        print(f"[SUCCESS] Created '{data['title']}'")
    else:
        # Update if already exists
        lp.location = data['location']
        lp.image = data['image']
        lp.save()
        print(f"[INFO] Updated '{data['title']}'")

print("Done.")
