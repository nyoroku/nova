import re
from django.db import migrations, models

MONEY = re.compile(r'(?:KES|Ksh|USD|\$)\s*[\d,]+', re.I)


def migrate_copy(apps, schema_editor):
    Article = apps.get_model('content', 'GuideArticle')
    QA = apps.get_model('content', 'QuestionAnswer')
    for article in Article.objects.all():
        if not MONEY.search(article.body + article.direct_quick_answer):
            continue
        original = article.body
        title = article.title.lower()
        route = 'crescent-island' if 'crescent' in title else 'groups-events' if 'group' in title or 'corporate' in title else 'private-charter' if 'private' in title or 'full day' in title else 'classic-lake-safari'
        intro = ('A useful boat-ride budget starts with the exact experience, boat arrangement and party size. '
                 'Compare the duration and what is included before comparing headline prices.')
        sections = [
            ('Choose the correct pricing unit', 'A private-boat rate covers the stated passenger limit. A shared-seat rate applies per person. Group options can have a minimum party size. Choose the actual option rather than multiplying or comparing unrelated headline prices.'),
            ('Check the complete cost', 'Ask for an itemized quote covering the boat service, any mandatory attraction admission, hotel positioning, road transport and optional extras. Costs paid directly to an attraction are still part of your trip budget.'),
            ('Match the experience to your plans', 'Check the option’s duration, departure point, passenger limits and equipment requirements. Tell Nova children’s ages and any boarding needs. Hotel departures require access and permission checks.'),
            ('Confirm before paying', 'An availability enquiry does not reserve a boat. Confirm your departure, total price, cancellation terms and weather arrangements with Nova before making payment.'),
        ]
        if route == 'crescent-island':
            sections.insert(1, ('Crescent Island admission', 'Nova’s boat crossing and the sanctuary admission are separate services unless your confirmed quote bundles them. Admission depends on visitor category and eligibility. The prices page shows the configured fee schedule, source and verification date.'))
        if route == 'groups-events':
            sections.insert(1, ('Group logistics', 'Discuss total party size, individual boat limits, launch timing and passenger allocation. Hotel positioning and transport for several boats require a group quote.'))
        article.previous_price_copy = original
        article.body = '<p>' + intro + '</p>' + ''.join('<h2>' + heading + '</h2><p>' + text + '</p>' for heading, text in sections)
        article.body += f'<h2>Current rates and relevant experiences</h2><p><a href="/prices/">View the current option-specific rates and external fees</a>, or <a href="/boat-rides/{route}/">explore the relevant Nova experience</a>.</p>'
        article.direct_quick_answer = intro + ' Use Nova’s current prices page for option-specific rates and external fees.'
        article.save(update_fields=['body', 'previous_price_copy', 'direct_quick_answer'])
    for qa in QA.objects.all():
        if MONEY.search(qa.answer + qa.plain_answer):
            qa.previous_price_copy = qa.answer
            qa.answer = '<p>Choose an activity and booking option on <a href="/prices/">Nova’s current prices page</a>. It shows the pricing unit, duration, passenger limits and separate attraction fees. Ask Nova to confirm availability and your complete quote, including any hotel or transport charges.</p>'
            qa.plain_answer = 'Current rates depend on the activity, booking option and party. See Nova’s prices page and confirm the full quote before booking.'
            qa.save(update_fields=['answer', 'plain_answer', 'previous_price_copy'])


class Migration(migrations.Migration):
    dependencies = [('content', '0002_reviewsnapshot_captain_certification_issuer_and_more')]
    operations = [
        migrations.AddField(model_name='guidearticle', name='previous_price_copy', field=models.TextField(blank=True, editable=False)),
        migrations.AddField(model_name='questionanswer', name='previous_price_copy', field=models.TextField(blank=True, editable=False)),
        migrations.RunPython(migrate_copy, migrations.RunPython.noop),
    ]
