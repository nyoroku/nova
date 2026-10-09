"""Read-only smoke verification of the normal local catalogue and generated reports."""
import os
import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','boats.settings')
import django
django.setup()
from django.test import Client
from tours.models import Tour,ServiceIntent,ActivityImage
from content.models import GuideArticle,QuestionAnswer
from django.core.management import call_command

client=Client()
routes=['/','/boat-rides/','/prices/','/services/','/book/','/about/']+[t.get_absolute_url() for t in Tour.objects.published()]
pages=[]
for route in routes:
    response=client.get(route)
    assert response.status_code==200,(route,response.status_code)
    soup=BeautifulSoup(response.content,'html.parser')
    assert len(soup.find_all('h1'))==1,(route,'H1 count')
    assert '?' not in soup.find('link',rel='canonical')['href'],route
    for script in soup.find_all('script',type='application/ld+json'):
        json.loads(script.string)
    pages.append({'route':route,'status':response.status_code,'h1':soup.h1.get_text(' ',strip=True)})
for slug in ['sunrise-wildlife','full-lake-explorer']:
    assert client.get('/boat-rides/'+slug+'/').status_code==404
assert ServiceIntent.objects.filter(level='PRIMARY').count()==15
assert ServiceIntent.objects.filter(level='SECONDARY').count()==15
money=re.compile(r'(?:KES|Ksh|USD|\$)\s*[\d,]+',re.I)
stale=[]
for article in GuideArticle.objects.filter(is_active=True):
    text=BeautifulSoup(article.body,'html.parser').get_text(' ')+' '+article.direct_quick_answer+' '+article.excerpt
    if money.search(text):stale.append(article.slug)
for qa in QuestionAnswer.objects.filter(is_active=True):
    if money.search(BeautifulSoup(qa.answer,'html.parser').get_text(' ')+' '+qa.plain_answer):stale.append('FAQ:'+str(qa.pk))
assert not stale,('Stale price copy',stale)
call_command('activity_reports')
summary={'pages':pages,'activities':Tour.objects.count(),'public_activities':Tour.objects.published().count(),
    'draft_activities':Tour.objects.filter(status='DRAFT').count(),'service_intents':ServiceIntent.objects.count(),
    'published_gallery_images':ActivityImage.objects.filter(is_published=True).count(),'stale_price_copy':stale,
    'google_ready_activities':sum(not t.publication_issues(google=True) for t in Tour.objects.all())}
target=ROOT/'outputs'/'activity-rebuild'/'smoke.json'
target.write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
