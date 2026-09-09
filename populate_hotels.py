import os
import django
import shutil
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from accommodation.models import PartnerHotel, HotelImage

def populate():
    # Delete existing hotels to start fresh
    PartnerHotel.objects.all().delete()
    
    sample_image_path = r"C:/Users/Administrator/.gemini/antigravity/brain/b17d6bef-0d2e-4086-b993-3f13be745b17/naivasha_hotel_sample_1769952335279.png"
    
    hotels_data = [
        {
            "name": "Naivasha Lakefront Resort",
            "slug": "naivasha-lakefront-resort",
            "description": "<p>Experience luxury at the edge of Lake Naivasha. Our resort offers stunning views, premium amenities, and exclusive boat tour packages with Rafiki.</p><p>Enjoy guided bird walks, hippos spotting from your balcony, and world-class dining.</p>",
            "location": "North Lake Road, Naivasha",
            "website_url": "https://example.com/naivasha-resort"
        },
        {
            "name": "Crescent View Lodge",
            "slug": "crescent-view-lodge",
            "description": "<p>A boutique lodge nestled in the heart of Naivasha's wild beauty. Perfect for families and nature enthusiasts who love the lake.</p>",
            "location": "South Lake, Naivasha",
            "website_url": "https://example.com/crescent-view"
        },
        {
            "name": "Enashipai Resort & Spa",
            "slug": "enashipai-resort-spa",
            "description": "<p>A place of happiness. This award-winning resort offers a unique blend of nature and modern luxury, just minutes from Rafiki boat launch.</p>",
            "location": "Moi South Lake Road",
            "website_url": "https://example.com/enashipai"
        },
        {
            "name": "Sawela Lodge",
            "slug": "sawela-lodge",
            "description": "<p>Serene and spacious. Sawela Lodge provides a relaxing escape with manicured lawns and direct access to lake activities.</p>",
            "location": "South Lake Road",
            "website_url": "https://example.com/sawela"
        },
        {
            "name": "Naivasha Simba Lodge",
            "slug": "naivasha-simba-lodge",
            "description": "<p>Immerse yourself in the wild. Our lodge offers a rustic yet comfortable experience with frequent wildlife sightings on the grounds.</p>",
            "location": "North Lake, Naivasha",
            "website_url": "https://example.com/simba-lodge"
        }
    ]

    for data in hotels_data:
        hotel = PartnerHotel.objects.create(
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
            location=data["location"],
            website_url=data["website_url"],
            is_active=True
        )
        
        if os.path.exists(sample_image_path):
            with open(sample_image_path, 'rb') as f:
                hotel.main_image.save(f"{hotel.slug}.png", File(f), save=True)
                
            # Add a few gallery images using the same placeholder
            for i in range(3):
                with open(sample_image_path, 'rb') as f:
                    img = HotelImage.objects.create(hotel=hotel, caption=f"View {i+1} from {hotel.name}", order=i)
                    img.image.save(f"{hotel.slug}_gallery_{i}.png", File(f), save=True)
                    
        print(f"Created {hotel.name} with gallery.")

if __name__ == "__main__":
    populate()
