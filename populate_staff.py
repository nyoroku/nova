import os
import django
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from reputation.models import StaffMember
from testimonials.models import Testimonial

def populate():
    # Clear existing
    StaffMember.objects.all().delete()
    
    staff_data = [
        {"name": "Captain James", "role": "CAPTAIN", "bio": "James has over 15 years of experience navigating Lake Naivasha. He is known for his deep knowledge of bird species and his calm, safe handling of the boat."},
        {"name": "Guide Sarah", "role": "GUIDE", "bio": "Sarah graduated with a degree in Wildlife Management and loves sharing stories about the lake's ecosystem. She's a favorite for families with children."},
        {"name": "Captain Moses", "role": "CAPTAIN", "bio": "Moses specializes in sunrise photography tours. He knows exactly where and when the light hits the hippos just right."},
        {"name": "Guide Amad", "role": "GUIDE", "bio": "Amad is our high-energy guide who makes every tour a celebration. Ask him about the history of Crescent Island!"},
    ]

    for data in staff_data:
        member = StaffMember.objects.create(
            name=data["name"],
            role=data["role"],
            bio=data["bio"]
        )
        print(f"Created {member.name} - QR generated: {bool(member.qr_code)}")
        
        # Add some initial reviews
        Testimonial.objects.create(
            customer_name="John Doe",
            rating=5,
            testimonial_text=f"Amazing trip with {member.name}! Truly professional.",
            staff_member=member,
            is_active=True
        )
        Testimonial.objects.create(
            customer_name="Jane Smith",
            rating=4,
            testimonial_text=f"Great experience, would recommend {member.name}.",
            staff_member=member,
            is_active=True
        )

if __name__ == "__main__":
    populate()
