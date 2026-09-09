import os
import django
import sys
from django.utils.text import slugify
from django.core.files import File

# Add current directory to path
sys.path.append(os.getcwd())

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.contrib.auth.models import User
from seo.models import FAQ, LocalPage
from services.models import Service
from bookings.models import Tour
from accommodation.models import PartnerHotel
from reputation.models import StaffMember
from testimonials.models import Testimonial
from blog.models import Post

def seed_final():
    print("--- Starting Final Seeding & Image Assignment ---")

    # 1. Superuser
    if not User.objects.filter(username='riziki').exists():
        seed_password = os.environ.get('DJANGO_SEED_RIZIKI_PASSWORD')
        if not seed_password:
            raise RuntimeError('Set DJANGO_SEED_RIZIKI_PASSWORD before creating this seed superuser.')
        User.objects.create_superuser('riziki', 'rizikiway@gmail.com', seed_password)
    
    # 2. Tours with Images
    tours_data = [
        ("Classic Lake Safari", 1.5, 3000, 60, 7, "Explore the main lake and see the famous hippo pods.", 'tour_images/hippo_bird.png'),
        ("Hippo & Bird Safari", 1.5, 3000, 60, 7, "Explore the main lake and see the famous hippo pods.", 'tour_images/hippo_bird.png'),
        ("Crescent Island Walking Safari", 2.0, 4500, 85, 6, "Combine a boat ride with a walking safari on Crescent Island.", 'tour_images/crescent_walking.png'),
        ("Photography Safari", 3.0, 5500, 100, 4, "A deep dive into the 400+ bird species found on Lake Naivasha.", 'tour_images/photography.png'),
        ("Full Day Lake Adventure", 6.0, 12000, 200, 8, "A complete exploration of Lake Naivasha including Oloidien.", 'tour_images/full_day.png'),
        ("Sunset Cruise", 1.5, 4000, 70, 5, "Romantic and scenic sunset cruises.", 'tour_images/sunset_cruise.png'),
        ("Private Charter", 2.0, 8000, 150, 6, "Private hire for groups and special events.", 'tour_images/private_charter.png'),
    ]
    
    for name, dur, p_res, p_int, max_p, desc, img in tours_data:
        t, created = Tour.objects.get_or_create(
            slug=slugify(name),
            defaults={
                'name': name,
                'duration_hours': dur,
                'price_resident': p_res,
                'price_international': p_int,
                'max_people': max_p,
                'description': desc,
                'image': img,
                'is_active': True
            }
        )
        if not created:
            t.name = name
            t.image = img
            t.save()
            print(f"Updated Tour: {name}")
        else:
            print(f"Created Tour: {name}")

    # 3. Destinations with Images
    dests_data = [
        ("Boat Rides Naivasha", "Lake Naivasha", "Boat rides Naivasha", "Experience the best boat tours on Lake Naivasha.", 'location_images/boat_rides.png'),
        ("Crescent Island Tours", "Crescent Island", "Crescent Island tours", "Walking safaris and bird watching on Crescent Island.", 'location_images/crescent_island.png'),
        ("Sunset Cruises Naivasha", "Lake Naivasha", "Sunset cruises Naivasha", "Unforgettable sunset experiences.", 'location_images/sunset_details.png'), # Fallback check
    ]
    
    for title, loc, key, content, img in dests_data:
        lp, created = LocalPage.objects.get_or_create(
            slug=slugify(title),
            defaults={
                'title': title,
                'location': loc,
                'primary_keyword': key,
                'content': f'<p>{content}</p>',
                'image': img,
                'is_active': True
            }
        )
        if not created:
            lp.image = img
            lp.save()
            print(f"Updated Destination: {title}")
        else:
            print(f"Created Destination: {title}")

    # 4. Services
    services = [
        ("Private Boat Tours", "fas fa-ship", "Exclusive boat tours tailored to your group's preferences."),
        ("Bird Watching", "fas fa-dove", "Expert-led bird watching tours."),
        ("Sunset Cruises", "fas fa-sun", "Scenic sunset cruises."),
    ]
    for title, icon, desc in services:
        Service.objects.get_or_create(
            slug=slugify(title),
            defaults={'title': title, 'icon_class': icon, 'description': f'<p>{desc}</p>', 'is_active': True}
        )

    # 5. FAQs, Hotels, Staff, etc. (Keep if needed or just minimal)
    # ... assuming they are fine from previous run, or just run them again
    
    print("--- Seeding & Assignment Completed ---")

if __name__ == "__main__":
    seed_final()
