import os
import django
import sys
from django.utils.text import slugify
from decimal import Decimal

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

def seed_data():
    print("--- Starting Data Seeding for Rafiki Boat Rides ---")

    # 1. Superuser
    if not User.objects.filter(username='riziki').exists():
        try:
            from decouple import config
            seed_password = os.environ.get('DJANGO_SEED_RIZIKI_PASSWORD') or config('DJANGO_SEED_RIZIKI_PASSWORD', default=None)
        except Exception:
            seed_password = os.environ.get('DJANGO_SEED_RIZIKI_PASSWORD')
        if not seed_password:
            seed_password = "RizikiPass123!"
        User.objects.create_superuser('riziki', 'rizikiway@gmail.com', seed_password)
        print("Created Superuser: riziki")
    else:
        print("Superuser riziki already exists.")

    # 2. FAQs
    faqs = [
        ("How long are the boat rides?", "Our rides vary from 1 hour to a full day, depending on the tour you choose."),
        ("Is it safe for children?", "Yes, we provide life jackets for all ages and our captains are highly trained in safety."),
        ("Can we see hippos?", "Absolutely! Lake Naivasha is famous for its hippos, and we know the best spots to find them safely."),
    ]
    for q, a in faqs:
        FAQ.objects.get_or_create(question=q, defaults={'answer': f'<p>{a}</p>', 'plain_answer': a, 'is_active': True})
    print(f"Seeded {len(faqs)} FAQs.")

    # 3. LocalPages (Destinations)
    destinations = [
        ("Crescent Island", "Naivasha", "Crescent Island Naivasha boat ride", "Crescent Island is a private island sanctuary on Lake Naivasha, famous for its abundance of plains game."),
        ("Hippo Point", "Lake Naivasha", "Hippo Point Lake Naivasha", "Hippo Point is a scenic spot on the lake known for large hippo pods and diverse birdlife."),
        ("Elsamere", "South Lake", "Elsamere boat tour", "Former home of Joy Adamson, Elsamere offers a peaceful retreat and conservation history."),
    ]
    for title, loc, key, content in destinations:
        LocalPage.objects.get_or_create(
            title=title, 
            defaults={
                'location': loc, 
                'primary_keyword': key, 
                'content': f'<p>{content}</p>', 
                'is_active': True
            }
        )
    print(f"Seeded {len(destinations)} Destinations.")

    # 4. Services
    services = [
        ("Private Boat Tours", "fas fa-ship", "Exclusive boat tours tailored to your group's preferences."),
        ("Bird Watching", "fas fa-dove", "Expert-led bird watching tours on the lake's rich ecosystem."),
        ("Sunset Cruises", "fas fa-sun", "Romantic and scenic sunset cruises for an unforgettable evening."),
    ]
    for title, icon, desc in services:
        slug = slugify(title)
        Service.objects.get_or_create(
            slug=slug, 
            defaults={
                'title': title,
                'icon_class': icon, 
                'description': f'<p>{desc}</p>', 
                'is_active': True
            }
        )
    print(f"Seeded {len(services)} Services.")

    # 5. Tours
    tours = [
        ("Classic Lake Safari", 1.5, 3000, 60, 7, "Explore the main lake and see the famous hippo pods."),
        ("Crescent Island Sanctuary Tour", 2.0, 4500, 85, 6, "Combine a boat ride with a walking safari on Crescent Island."),
        ("Birders Paradise Tour", 3.0, 5500, 100, 4, "A deep dive into the 400+ bird species found on Lake Naivasha."),
    ]
    for name, dur, price_res, price_int, max_p, desc in tours:
        slug = slugify(name)
        Tour.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'duration_hours': dur,
                'price_resident': price_res,
                'price_international': price_int,
                'max_people': max_p,
                'description': desc,
                'is_active': True
            }
        )
    print(f"Seeded {len(tours)} Tours.")

    # 6. Hotels
    hotels = [
        ("Naivasha Lakefront Resort", "North Lake Road, Naivasha", "https://example.com/resort"),
        ("Sawela Lodge", "South Lake Road", "https://example.com/sawela"),
        ("Enashipai Resort & Spa", "Moi South Lake Road", "https://example.com/enashipai"),
    ]
    for name, loc, url in hotels:
        slug = slugify(name)
        PartnerHotel.objects.get_or_create(
            slug=slug, 
            defaults={
                'name': name,
                'location': loc, 
                'website_url': url, 
                'is_active': True
            }
        )
    print(f"Seeded {len(hotels)} Partner Hotels.")

    # 7. Staff
    staff = [
        ("Captain Steve", "CAPTAIN", "Over 10 years of experience navigating Lake Naivasha."),
        ("Guide Sarah", "GUIDE", "Expert in local bird species and conservation history."),
    ]
    for name, role, bio in staff:
        StaffMember.objects.get_or_create(name=name, defaults={'role': role, 'bio': bio})
    print(f"Seeded {len(staff)} Staff Members.")

    # 8. Testimonials
    testimonials = [
        ("John Doe", "USA", 5, "Amazing experience! The captain was so knowledgeable and we saw so many hippos."),
        ("Jane Smith", "UK", 5, "The sunset cruise was the highlight of our trip. Truly magical."),
        ("Peter Kamau", "KE", 4, "Great local tour. The boat was clean and safety was a priority."),
    ]
    for name, country, rating, comment in testimonials:
        Testimonial.objects.get_or_create(
            customer_name=name, 
            customer_country=country, 
            defaults={
                'rating': rating, 
                'testimonial_text': comment, 
                'is_active': True
            }
        )
    print(f"Seeded {len(testimonials)} Testimonials.")

    # 9. Blog Posts
    author = User.objects.get(username='riziki')
    posts = [
        ("Discover the Magic of Lake Naivasha", "Naivasha is not just a lake; it is a vibrant ecosystem teeming with life. From the playful hippos to the majestic fish eagles, every moment here is a story waiting to be told."),
    ]
    for title, content in posts:
        Post.objects.get_or_create(
            title=title, 
            defaults={
                'author': author, 
                'content': f'<p>{content}</p>', 
                'status': 'published'
            }
        )
    print(f"Seeded {len(posts)} Blog Posts.")

    print("--- Seeding Completed Successfully! ---")

if __name__ == "__main__":
    seed_data()
