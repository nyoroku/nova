"""
Verify the seeded TOFU/MOFU/BOFU funnel content and internal linking engine.
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from blog.models import Post
from seo.models import FAQ, LocalPage, InternalLink

print("=== VERIFYING FUNNEL SEO CONTENT SEEDING ===")

# 1. Verify Blogs
expected_blogs = [
    'things-to-do-naivasha-madaraka-day-holidays',
    'lake-naivasha-boat-ride-comparison-rafiki-watamu-njovic',
    'how-to-book-safest-affordable-hippo-boat-safari'
]

print("\n--- Checking Blogs ---")
for slug in expected_blogs:
    try:
        post = Post.objects.get(slug=slug)
        words = len(post.content.split())
        print(f"  [PASS] Blog '{post.title}' found | Word Count: {words}")
        # Test linked content
        linked = post.linked_content
        if "href" in linked:
            print("         -> Verified: Contains auto-linked internal keywords!")
        else:
            print("         -> WARNING: No links generated. Check keywords & content matches.")
    except Post.DoesNotExist:
        print(f"  [FAIL] Blog with slug '{slug}' not found!")

# 2. Verify Local Pages
expected_pages = [
    'crescent-island-walking-safari',
    'karagita-public-beach',
    'sanctuary-farm-lake-naivasha'
]

print("\n--- Checking Local Pages ---")
for slug in expected_pages:
    try:
        page = LocalPage.objects.get(slug=slug)
        words = len(page.content.split())
        print(f"  [PASS] Page '{page.title}' found | Word Count: {words}")
        linked = page.linked_content
        if "href" in linked:
            print("         -> Verified: Contains auto-linked internal keywords!")
        else:
            print("         -> WARNING: No links generated. Check keywords & content matches.")
    except LocalPage.DoesNotExist:
        print(f"  [FAIL] Local Page with slug '{slug}' not found!")

# 3. Verify FAQs
expected_faqs = [
    "How do I book a boat ride for Madaraka Day, Easter, or Christmas holidays?",
    "How does Rafiki's pricing compare to Watamu and Njovic boat rides?",
    "Is a boat ride on Lake Naivasha safe during windy weather or afternoons?",
    "Can we eat fresh tilapia at Karagita Beach before or after our boat ride?",
    "Should I book a private boat charter or a shared group ride?"
]

print("\n--- Checking FAQs ---")
for question in expected_faqs:
    try:
        faq = FAQ.objects.get(question=question)
        print(f"  [PASS] FAQ '{faq.question}' found | Order: {faq.order} | Intent: {faq.search_intent}")
    except FAQ.DoesNotExist:
        print(f"  [FAIL] FAQ '{question}' not found!")

print("\n--- Verification Complete ---")
