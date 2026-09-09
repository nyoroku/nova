import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from blog.models import Post
from seo.models import FAQ, LocalPage

print("=== CURRENT DATABASE CONTENT SURVEY ===")
print(f"Total Blog Posts: {Post.objects.count()}")
print(f"Total FAQs: {FAQ.objects.count()}")
print(f"Total Local Pages: {LocalPage.objects.count()}")

print("\n--- Existing Local Page Slugs ---")
for lp in LocalPage.objects.all():
    print(f"  - {lp.slug} ({lp.title})")
