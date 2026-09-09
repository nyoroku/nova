import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from services.models import Service
from bookings.models import Tour
from seo.models import FAQ, LocalPage

def fix_db():
    print("=== Cleaning Spot Fishing typos from Database ===")
    
    # 1. Clean up Services
    old_services = Service.objects.filter(slug='spot-fishing-experience')
    if old_services.exists():
        print(f"Deleting old service: {old_services.first()}")
        old_services.delete()
        
    # 2. Check Tours (in case any tour was named spot-fishing)
    old_tours = Tour.objects.filter(slug='spot-fishing-experience')
    if old_tours.exists():
        print(f"Deleting old tour: {old_tours.first()}")
        old_tours.delete()
        
    # 3. Rename any text references in FAQs
    faq_updated = 0
    for faq in FAQ.objects.all():
        updated = False
        if "spot fishing" in faq.question.lower():
            faq.question = faq.question.replace("Spot fishing", "Sport fishing").replace("spot fishing", "sport fishing").replace("Spot Fishing", "Sport Fishing")
            updated = True
        if "spot fishing" in faq.answer.lower():
            faq.answer = faq.answer.replace("Spot fishing", "Sport fishing").replace("spot fishing", "sport fishing").replace("Spot Fishing", "Sport Fishing")
            updated = True
        if "spot fishing" in faq.plain_answer.lower():
            faq.plain_answer = faq.plain_answer.replace("Spot fishing", "Sport fishing").replace("spot fishing", "sport fishing").replace("Spot Fishing", "Sport Fishing")
            updated = True
            
        if updated:
            faq.save()
            faq_updated += 1
    print(f"Updated {faq_updated} FAQs.")

    # 4. Rename any text references in LocalPages
    page_updated = 0
    for page in LocalPage.objects.all():
        updated = False
        if "spot fishing" in page.title.lower():
            page.title = page.title.replace("Spot fishing", "Sport fishing").replace("spot fishing", "sport fishing").replace("Spot Fishing", "Sport Fishing")
            updated = True
        if "spot fishing" in page.content.lower():
            page.content = page.content.replace("Spot fishing", "Sport fishing").replace("spot fishing", "sport fishing").replace("Spot Fishing", "Sport Fishing")
            updated = True
            
        if updated:
            page.save()
            page_updated += 1
    print(f"Updated {page_updated} LocalPages.")
    
    print("=== Database Clean-up Complete ===")

if __name__ == "__main__":
    fix_db()
