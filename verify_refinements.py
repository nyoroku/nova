import os
import django
from django.test import Client

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

def verify():
    client = Client()
    
    # 1. Homepage Section
    print("Verifying Homepage...")
    response = client.get('/')
    content = response.content.decode('utf-8')
    if 'Stay Near the Lake' in content and 'hotelsSwiper' in content:
        print("  SUCCESS: Found 'Stay Near the Lake' and Swiper container.")
    else:
        print("  FAILURE: Missing refined homepage section.")

    # 2. Hotel List Design
    print("\nVerifying Hotel List...")
    response = client.get('/accommodation/')
    content = response.content.decode('utf-8')
    if 'Stay Near the Lake' in content and 'shadow-card' in content:
         print("  SUCCESS: Found updated title and card styling.")
    else:
        print("  FAILURE: Hotel list style not updated.")

    # 3. Hotel Detail & Gallery
    print("\nVerifying Hotel Detail (Enashipai)...")
    response = client.get('/accommodation/enashipai-resort-spa/')
    content = response.content.decode('utf-8')
    if 'hotelGallerySwiper' in content and 'Trusted Partner' in content:
        print("  SUCCESS: Found detail gallery swiper and clarified partner text.")
    else:
        print("  FAILURE: Detail page issues detected.")

if __name__ == "__main__":
    verify()
