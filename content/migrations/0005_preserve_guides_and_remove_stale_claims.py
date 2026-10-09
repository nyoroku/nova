import re
from html import escape
from bs4 import BeautifulSoup
from django.db import migrations

MONEY = re.compile(r'(?:KES|Ksh|USD|\$)\s*[\d,]+', re.I)
ATTACK = re.compile(r'extortion|beach tout|tourist scam|packed to maximum', re.I)
OVERCLAIM = re.compile(r'completely safe|100% safe|guaranteed sightings|zero wind|you will encounter', re.I)


def clean_guide(original):
    soup = BeautifulSoup(original, 'html.parser')
    # Keep original headings, images, links and non-price explanation. Replace only stale cost/claim blocks.
    for tag in reversed(soup.find_all(['p', 'li', 'td', 'th', 'caption'])):
        text = tag.get_text(' ', strip=True)
        if MONEY.search(text) or ATTACK.search(text):
            label = tag.find('strong')
            prefix = label.get_text(' ', strip=True) if label and not MONEY.search(label.get_text()) and not ATTACK.search(label.get_text()) else ''
            replacement = ('<strong>' + escape(prefix) + '</strong> ' if prefix else '')
            replacement += '<a href="/prices/">Check current option-specific rates and fees</a>. Confirm the complete quote with Nova before booking.'
            tag.clear()
            tag.append(BeautifulSoup(replacement, 'html.parser'))
        elif OVERCLAIM.search(text):
            tag.clear()
            tag.append('Lake conditions and wildlife sightings vary. Confirm your route, equipment and departure arrangements with Nova.')
    for heading in soup.find_all(['h2','h3','h4']):
        if ATTACK.search(heading.get_text()):
            heading.string = 'What to clarify before booking'
    return str(soup)


def forwards(apps, schema_editor):
    Article = apps.get_model('content','GuideArticle')
    QA = apps.get_model('content','QuestionAnswer')
    for article in Article.objects.all():
        original = article.previous_price_copy or article.body
        if not (MONEY.search(original) or ATTACK.search(original) or OVERCLAIM.search(original)):
            continue
        if not article.previous_price_copy:
            article.previous_price_copy = original
        article.body = clean_guide(original)
        for field in ['excerpt','direct_quick_answer','meta_description']:
            value = getattr(article, field)
            if MONEY.search(value) or ATTACK.search(value) or OVERCLAIM.search(value):
                setattr(article, field, 'Compare the activity, duration, pricing unit and inclusions. Check Nova’s current rates and confirm your complete quote before booking.')
        article.save(update_fields=['body','previous_price_copy','excerpt','direct_quick_answer','meta_description'])
    for qa in QA.objects.all():
        if OVERCLAIM.search(qa.answer + qa.plain_answer):
            if not qa.previous_price_copy:
                qa.previous_price_copy = qa.answer
            qa.answer = '<p>Weather, water conditions and wildlife sightings vary. Tell Nova your party’s ages and boarding needs, and confirm suitable equipment, the route and departure conditions before booking. Your captain’s briefing and properly fitted life jackets are required.</p>'
            qa.plain_answer = 'Confirm equipment, boarding needs and departure conditions with Nova. Weather and wildlife sightings vary.'
            qa.save(update_fields=['answer','plain_answer','previous_price_copy'])


class Migration(migrations.Migration):
    dependencies = [('content','0004_captain_verification_evidence_and_more')]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
