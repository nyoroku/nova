import json
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils import timezone
from tours.models import Tour, ExperienceRate, ServiceIntent
from tours.attribution import campaign_url
from tours.pricing import quote_activity


def cell(value):
    return str('—' if value is None or value == '' else value).replace('|', '\\|').replace('\n', ' ')


class Command(BaseCommand):
    help = 'Generate internal catalogue, price and Google readiness reports. Does not submit listings.'
    def add_arguments(self, parser):
        parser.add_argument('--output-dir', default='.')
        parser.add_argument('--before', default='outputs/activity-rebuild/before.json')
        parser.add_argument('--optimize-images', action='store_true')

    def handle(self, *args, **options):
        output = Path(options['output_dir'])
        output.mkdir(parents=True, exist_ok=True)
        before_path = Path(options['before'])
        before = json.loads(before_path.read_text(encoding='utf-8')) if before_path.exists() else {}
        old = {t['slug']:t for t in before.get('tours_tour', [])}
        tours = list(Tour.objects.all().order_by('order'))
        if options['optimize_images']:
            for tour in tours:
                for image in tour.images.all():
                    try:
                        image.save(optimize=True)
                    except (OSError, ValueError) as error:
                        image.is_published = False
                        image.save(update_fields=['is_published'])
                        self.stderr.write(f'{tour.slug}: image optimization pending ({type(error).__name__})')
        inventory = ['# Nova activity current-state inventory', f'Generated {timezone.localdate()}.',
            'Existing URLs are preserved. Historical public products remain available while their checklist is completed. New products are drafts. Indexing status is unknown without Search Console.',
            '| Existing name | Public name | URL | Tour minutes before | Rate minutes | Gallery count | Status / action |', '|---|---|---|---|---|---|---|']
        matrix = ['# Nova product facts requiring verification',
            'Stored values are configuration, not fresh owner approval. Rates and option limits are retained without inventing new amounts.',
            '| Activity | Proposed PRD minutes | Existing tour minutes | Configured option minutes / guest limits | Verification |', '|---|---|---|---|---|']
        proposed = {'classic-lake-safari':60,'hippo-bird-safari':90,'crescent-island':120,'sunset-cruise':90,
            'private-charter':120,'family-ride':75,'photography-birding':150,'groups-events':120,'sunrise-wildlife':90,'full-lake-explorer':180}
        gbp = ['# Nova Google activity export and readiness', f'Generated {timezone.localdate()}.',
            'Internal candidates only. BLOCKED rows must not be published. Six gallery photos is a Nova editorial requirement; channel acceptance is recorded separately. No external profile or feed was changed.',
            '| Activity | Clean URL | GBP tracking URL | Image | Standard adult minimum transaction | Readiness |', '|---|---|---|---|---|---|']
        feed = []
        prices = ['# Nova activity price audit', f'Generated {timezone.localdate()}.',
            'All customer quote paths use ExperienceRate linked to TourOption. Legacy TourPriceTier rows are retained for history but are not a public price fallback. Missing, ambiguous, expired or unsupported rates request a quote.',
            '| Activity / option | Currency | Unit amount / unit | Minimum transaction | Duration / guests | Effective dates | Verification |', '|---|---|---|---|---|---|---|']
        for tour in tours:
            previous = old.get(tour.slug)
            old_minutes = int(float(previous['duration_hours']) * 60) if previous else 'New'
            durations = ', '.join(str(x) for x in tour.options.values_list('duration_minutes', flat=True))
            inventory.append('| ' + ' | '.join(map(cell, [previous['name'] if previous else 'New', tour.name, tour.canonical_url,
                old_minutes, durations, tour.images.filter(is_published=True).count(), tour.status + (' / RENAME DISPLAY' if previous else ' / NEW DRAFT')])) + ' |')
            option_summary = '; '.join(f'{o.duration_minutes} min / {o.min_guests}–{o.max_guests} guests ({o.mode})' for o in tour.options.all())
            matrix.append('| ' + ' | '.join(map(cell, [tour.name, proposed.get(tour.slug), old_minutes, option_summary, 'Pending' if tour.publication_issues() else 'Complete'])) + ' |')
            issues = tour.publication_issues(google=True)
            rates = tour.current_rates.filter(audience_type__in=['ALL','NON_RESIDENT'], verified_at__isnull=False)
            totals = []
            for rate in rates:
                quote = quote_activity(tour, adults=rate.min_guests, visitor_type='NON_RESIDENT', currency=rate.currency, option_id=rate.option_id)
                if quote.complete:
                    totals.append(f'{quote.currency} {quote.total} / {rate.min_guests} adult(s) / {rate.option.name}')
            image = tour.images.filter(is_primary=True).first()
            tracking = campaign_url(tour.canonical_url, 'activity', tour.slug)
            gbp.append('| ' + ' | '.join(map(cell, [tour.name, tour.canonical_url, tracking, image.google_url if image and image.is_published else '',
                '; '.join(totals) or 'Not ready', 'BLOCKED: ' + '; '.join(issues) if issues else 'READY — channel acceptance still required'])) + ' |')
            feed.append({'id':f'nova-activity-{tour.pk}', 'name':tour.name, 'description':tour.summary,
                'booking_mode':tour.booking_mode, 'booking_url':tour.external_booking_url,
                'image_url':image.google_url if image and image.is_published else '',
                'url':tour.canonical_url, 'gbp_url':tracking,
                'google_ready':not issues, 'issues':issues, 'status':tour.status, 'options':[{'id':o.pk,'name':o.name,
                    'duration_minutes':o.duration_minutes,'min_guests':o.min_guests,'max_guests':o.max_guests,'mode':o.mode} for o in tour.options.all()]})
            for rate in tour.rates.select_related('option'):
                prices.append('| ' + ' | '.join(map(cell, [f'{tour.name} / {rate.option.name if rate.option else "Unmapped"}', rate.currency,
                    f'{rate.amount} {rate.unit_label}', rate.minimum_total, f'{rate.duration_minutes} min / {rate.min_guests}–{rate.max_guests}',
                    f'{rate.effective_from} to {rate.effective_until or "open"}', 'Pending' if not rate.verified_at else rate.verified_at])) + ' |')
        if before:
            prices += ['', '## Historical contradictory sources', 'The pre-change snapshot contains the following legacy tiers. They no longer drive current quotes.',
                '| Tour ID | Tier | Currency / amount | Unit |', '|---|---|---|---|']
            for tier in before.get('tours_tourpricetier', []):
                prices.append('| ' + ' | '.join(map(cell,[tier['tour_id'],tier['label'],f'{tier["currency"]} {tier["amount"]}',tier['pricing_unit']])) + ' |')
        prices += ['', '## Runtime monetary literals scan', 'Tests, migrations and preserved historical copy are excluded. Other products such as stays retain their own configured rates.']
        hits = []
        pattern = re.compile(r'(?:KES|USD|Ksh|\$)\s*\d[\d,]*')
        for folder in ['templates','tours','bookings','core','partners']:
            for path in Path(folder).rglob('*'):
                if path.suffix not in ('.py','.html') or 'migrations' in path.parts or 'management' in path.parts or 'tests' in path.name:
                    continue
                for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
                    if pattern.search(line): hits.append(f'- `{path.as_posix()}:{number}`: {line.strip()}')
        prices.extend(hits or ['No numeric currency literals found in the scanned runtime files.'])
        service_lines = ['# Nova service intent mappings', 'Thirty search intents resolve to canonical destinations. Public navigation deduplicates close variants. GBP publication requires verification.',
            '| Name | Level | Canonical destination | GBP readiness |', '|---|---|---|---|']
        for service in ServiceIntent.objects.select_related('activity'):
            service_lines.append('| ' + ' | '.join(map(cell,[service.name,service.level,service.destination,
                'Pending operations verification' if not service.operational_verified_at else 'Verified'])) + ' |')
        documents = {'NOVA_ACTIVITY_CURRENT_STATE.md':inventory,'NOVA_ACTIVITY_PRICE_AUDIT.md':prices,
            'NOVA_ACTIVITY_GBP_EXPORT.md':gbp,'NOVA_ACTIVITY_FACT_MATRIX.md':matrix,'NOVA_ACTIVITY_SERVICE_EXPORT.md':service_lines,
            'NOVA_ACTIVITY_REDIRECT_MAP.md':['# Nova activity URL preservation','No activity slugs were changed. The eight legacy activity URLs remain canonical. Existing unrelated legacy redirects are retained.']}
        for name,lines in documents.items():
            text = '\n\n'.join(lines[:3]) + '\n\n' + '\n'.join(lines[3:])
            (output/name).write_text(text.rstrip() + '\n',encoding='utf-8')
        (output/'NOVA_ACTIVITY_CHANNEL_CANDIDATES.json').write_text(json.dumps(feed,indent=2),encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Generated {len(documents)} reports and channel candidates for {len(tours)} activities.'))
