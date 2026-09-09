import os
import django
from django.utils import timezone
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from testimonials.models import Testimonial
from bookings.models import Tour
from reputation.models import StaffMember

def seed_reviews():
    print("=== Seeding Global Reviews ===")
    
    # 1. Clear existing testimonials to ensure a clean state
    print("Clearing old testimonials...")
    Testimonial.objects.all().delete()
    
    # Get available tours and staff
    tours = list(Tour.objects.all())
    staff = list(StaffMember.objects.all())
    
    if not tours:
        print("Error: No Tours found in database. Run tour seed scripts first.")
        return
        
    print(f"Found {len(tours)} tours and {len(staff)} staff members.")
    
    # Realistic global reviews dataset
    reviews_data = [
        {
            "customer_name": "Sarah Jenkins",
            "customer_country": "United Kingdom",
            "rating": 5,
            "testimonial_text": "An absolutely magical morning! We took the Classic Lake Safari and saw so many hippos up close. Our captain was extremely professional, pointing out the diverse birdlife. Lake Naivasha is a must-visit!",
            "tour_name": "Classic Lake Safari",
            "staff_name": "Captain James",
            "is_featured": True,
            "order": 1
        },
        {
            "customer_name": "David Miller",
            "customer_country": "United States",
            "rating": 5,
            "testimonial_text": "Crescent Island is a hidden gem. Walking among giraffes and zebras without any fences is an experience I will never forget. Guide Sarah was incredibly knowledgeable and great with the kids.",
            "tour_name": "Crescent Island Sanctuary Tour",
            "staff_name": "Guide Sarah",
            "is_featured": True,
            "order": 2
        },
        {
            "customer_name": "Elena Rostova",
            "customer_country": "Germany",
            "rating": 5,
            "testimonial_text": "We did the Sunset Cruise and the views were breathtaking. The golden light over the water, the silhouette of the acacia trees, and the sound of hippos in the distance made for a perfect evening. Highly recommended!",
            "tour_name": "Sunset Cruise",
            "staff_name": "Captain Moses",
            "is_featured": True,
            "order": 3
        },
        {
            "customer_name": "Kenji Tanaka",
            "customer_country": "Japan",
            "rating": 5,
            "testimonial_text": "A paradise for bird watchers! As a photographer, I was amazed by the number of African Fish Eagles we saw diving for fish. Captain Moses maneuvered the boat perfectly to get the best angles.",
            "tour_name": "Birders Paradise Tour",
            "staff_name": "Captain Moses",
            "is_featured": True,
            "order": 4
        },
        {
            "customer_name": "Mwangi Odhiambo",
            "customer_country": "Kenya",
            "rating": 5,
            "testimonial_text": "Excellent service and very clean boats. We felt safe throughout the tour. Guide Amad kept us entertained with fascinating history about the lake and Crescent Island. Safe, affordable, and fun!",
            "tour_name": "Classic Lake Safari",
            "staff_name": "Guide Amad",
            "is_featured": False,
            "order": 5
        },
        {
            "customer_name": "Chloe Dupont",
            "customer_country": "France",
            "rating": 5,
            "testimonial_text": "A wonderful walking safari on Crescent Island. Being so close to wild animals on foot was thrilling but felt very safe. Our guide Sarah answered all our questions. Highlight of our Kenya trip!",
            "tour_name": "Crescent Island Walking Safari",
            "staff_name": "Guide Sarah",
            "is_featured": False,
            "order": 6
        },
        {
            "customer_name": "Aarav Mehta",
            "customer_country": "India",
            "rating": 5,
            "testimonial_text": "The full day lake adventure is the best value. We saw dozens of birds, spent hours on Crescent Island, and had a beautiful lunch on the boat. Captain James is an expert navigator.",
            "tour_name": "Full Day Lake Adventure",
            "staff_name": "Captain James",
            "is_featured": False,
            "order": 7
        },
        {
            "customer_name": "Liam O'Connor",
            "customer_country": "Ireland",
            "rating": 4,
            "testimonial_text": "Very well organized tour. The boat was comfortable and life jackets were provided for everyone. We saw plenty of hippos and eagles. Guide Amad was fantastic. Highly recommended for families.",
            "tour_name": "Hippo & Bird Safari",
            "staff_name": "Guide Amad",
            "is_featured": False,
            "order": 8
        },
        {
            "customer_name": "Sophia van den Berg",
            "customer_country": "Netherlands",
            "rating": 5,
            "testimonial_text": "Stunning private charter experience. It was customized to our pace and interests. We got amazing pictures of the sunrise and the fish eagles. Thank you Captain Moses for your patience!",
            "tour_name": "Private Charter",
            "staff_name": "Captain Moses",
            "is_featured": True,
            "order": 9
        },
        {
            "customer_name": "Michael Ndlovu",
            "customer_country": "South Africa",
            "rating": 5,
            "testimonial_text": "Excellent bird watching tour. We spotted kingfishers, pelicans, and the iconic fish eagle. The boat captain was very skilled at navigating near the shoreline. Will definitely book again.",
            "tour_name": "Birders Paradise Tour",
            "staff_name": "Captain James",
            "is_featured": False,
            "order": 10
        },
        {
            "customer_name": "Isabella Rossi",
            "customer_country": "Italy",
            "rating": 5,
            "testimonial_text": "We booked a private boat ride for our honeymoon sunset. It was incredibly romantic and peaceful. The crew even had a small surprise for us! Memories to last a lifetime.",
            "tour_name": "Sunset Cruise",
            "staff_name": "Captain James",
            "is_featured": False,
            "order": 11
        },
        {
            "customer_name": "Ryan Campbell",
            "customer_country": "Australia",
            "rating": 5,
            "testimonial_text": "Incredible value! The walking safari with Guide Sarah was highlight of my trip. We saw giraffes, wildebeests, and waterbucks just meters away. Friendly staff and professional setup.",
            "tour_name": "Crescent Island Walking Safari",
            "staff_name": "Guide Sarah",
            "is_featured": False,
            "order": 12
        }
    ]
    
    # Create the records
    for item in reviews_data:
        # Find matching tour
        matched_tour = None
        for t in tours:
            if t.name.lower() == item["tour_name"].lower():
                matched_tour = t
                break
        
        # Find matching staff
        matched_staff = None
        for s in staff:
            if s.name.lower() == item["staff_name"].lower():
                matched_staff = s
                break
        
        testimonial = Testimonial.objects.create(
            customer_name=item["customer_name"],
            customer_country=item["customer_country"],
            rating=item["rating"],
            testimonial_text=item["testimonial_text"],
            tour=matched_tour,
            staff_member=matched_staff,
            is_active=True,
            is_featured=item["is_featured"],
            order=item["order"],
            date_added=timezone.now()
        )
        print(f"Seeded review from {testimonial.customer_name} ({testimonial.customer_country}) - Tour: {item['tour_name']}")

    print("=== Reviews Seeding Complete ===")

if __name__ == "__main__":
    seed_reviews()
