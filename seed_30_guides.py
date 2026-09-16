# c:\nova\seed_30_guides.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from content.models import GuideArticle, Captain
from content.articles_data.cluster1_pricing import ARTICLES as CLUSTER1
from content.articles_data.cluster2_day_trips import ARTICLES as CLUSTER2
from content.articles_data.cluster3_crescent_island import ARTICLES as CLUSTER3
from content.articles_data.cluster4_reviews_safety import ARTICLES as CLUSTER4
from content.articles_data.cluster5_hotel_logistics_faq import ARTICLES as CLUSTER5
from content.articles_data.article_expander import enrich_article

ALL_ARTICLES = CLUSTER1 + CLUSTER2 + CLUSTER3 + CLUSTER4 + CLUSTER5

print(f"Total articles to process: {len(ALL_ARTICLES)}")

created_count = 0
updated_count = 0

for i, data in enumerate(ALL_ARTICLES, 1):
    title = data['title']
    slug = data['slug']
    category = data.get('category', 'PLANNING')
    raw_body = data['body'].strip()
    enriched_body = enrich_article(slug, title, raw_body, category)
    words = len(enriched_body.split())
    
    article, created = GuideArticle.objects.update_or_create(
        slug=slug,
        defaults={
            'title': title,
            'excerpt': data['excerpt'],
            'body': enriched_body,
            'author': data.get('author', 'Captain Aizo Gateru'),
            'reviewer': data.get('reviewer', 'Senior Captain Team'),
            'category': category,
            'direct_quick_answer': data.get('direct_quick_answer', ''),
            'is_featured': data.get('is_featured', False),
            'is_active': True,
            'seo_title': data.get('seo_title', title[:70]),
            'meta_description': data.get('meta_description', data['excerpt'][:160]),
        }
    )
    status = "CREATED" if created else "UPDATED"
    if created:
        created_count += 1
    else:
        updated_count += 1
    print(f"[{i:02d}/30] {status}: '{title[:40]}...' | Words: {words} | Cat: {article.category}")

print(f"\nSeeding complete: {created_count} created, {updated_count} updated. Total GuideArticles in DB: {GuideArticle.objects.count()}")
