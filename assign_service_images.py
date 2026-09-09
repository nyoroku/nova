import os
import django
import sys

sys.path.append('c:/Users/Administrator/PycharmProjects/boats')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from services.models import Service

# Map categories to images
image_map = {
    'nature_education.png': [
        'Guided Nature Interpretation', 
        'School Educational Tours'
    ],
    'corporate_events.png': [
        'Corporate Team-Building', 
        'Wedding & Events'
    ],
    'adventure_fishing.png': [
        'Photography & Filming', 
        'Fishing Expeditions'
    ]
}

print("Assigning images to Services...")

for img_name, titles in image_map.items():
    db_path = f"service_images/{img_name}"
    for title in titles:
        try:
            service = Service.objects.get(title=title)
            service.image = db_path
            service.save()
            print(f"[SUCCESS] Assigned {img_name} to '{title}'")
        except Service.DoesNotExist:
            print(f"[WARNING] Service '{title}' not found!")
            
print("Done.")
