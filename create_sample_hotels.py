import os
import django
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from accommodation.models import PartnerHotel, HotelImage

def create_sample_data():
    # Create a partner hotel
    hotel, created = PartnerHotel.objects.get_or_create(
        name="Naivasha Lakefront Resort",
        slug="naivasha-lakefront-resort",
        defaults={
            "description": "<p>Experience luxury at the edge of Lake Naivasha. Our resort offers stunning views, premium amenities, and exclusive boat tour packages.</p><p>Enjoy guided bird walks, hippos spotting from your balcony, and world-class dining.</p>",
            "location": "North Lake Road, Naivasha",
            "website_url": "https://example.com/naivasha-resort",
            "is_active": True
        }
    )
    
    if created:
        # Add main image if you have one, or just let it be blank for now
        # For simplicity in this script, we'll assume we can't easily attach the generated image here
        # but the logic is there.
        print(f"Created hotel: {hotel.name}")
        
    # Create another one
    hotel2, created2 = PartnerHotel.objects.get_or_create(
        name="Crescent View Lodge",
        slug="crescent-view-lodge",
        defaults={
            "description": "<p>A boutique lodge nestled in the heart of Naivasha's wild beauty. Perfect for families and nature enthusiasts.</p>",
            "location": "South Lake, Naivasha",
            "website_url": "https://example.com/crescent-lodge",
            "is_active": True
        }
    )
    if created2:
        print(f"Created hotel: {hotel2.name}")

if __name__ == "__main__":
    create_sample_data()
