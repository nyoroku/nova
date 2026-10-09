from django.utils import timezone
from .pricing import quote_activity


def publication_issues(tour, google=False):
    issues = []
    if not tour.operational_verified_at or not tour.verification_evidence or not tour.operations_owner:
        issues.append('Confirm operational facts, evidence and responsible owner.')
    if not tour.seo_title or not tour.meta_description:
        issues.append('Complete the search title and description.')
    if not tour.summary or not tour.body or not tour.meeting_point:
        issues.append('Complete the overview, experience and meeting instructions.')
    if not tour.safety_briefing or not tour.weather_policy or not tour.cancellation_policy or not tour.accessibility_notes:
        issues.append('Confirm safety, weather, cancellation and boarding/accessibility policies.')
    for kind, minimum in [('HIGHLIGHT', 4), ('INCLUDED', 3), ('EXCLUDED', 2)]:
        if tour.details.filter(kind=kind).count() < minimum:
            issues.append(f'Add at least {minimum} {kind.lower()} items.')
    if not tour.itinerary_steps.exists() or tour.faqs.count() < 5:
        issues.append('Add a typical itinerary and at least five activity FAQs.')
    images = tour.images.filter(is_published=True)
    if images.count() < 6 or images.count() > 15:
        issues.append('Use 6–15 relevant gallery images (Nova editorial requirement).')
    primary = images.filter(is_primary=True).first()
    if not primary:
        issues.append('Choose exactly one published primary image.')
    if images.filter(rights_confirmed=False).exists() or images.filter(alt_text='').exists():
        issues.append('Confirm image rights/guest consent and descriptive alt text.')
    options = tour.options.filter(is_active=True)
    if not options.exists():
        issues.append('Add a real booking option.')
    for option in options:
        if not option.verified_at or not option.verification_evidence:
            issues.append(f'Confirm duration and capacity for {option.name}.')
        rates = tour.current_rates.filter(option=option)
        if not rates.exists() or rates.filter(verified_at__isnull=True).exists() or rates.filter(verification_evidence='').exists():
            issues.append(f'Confirm current prices for {option.name}.')
        seen = set()
        for rate in rates:
            key = (rate.currency, rate.audience_type)
            if key in seen:
                issues.append(f'Resolve overlapping current rates for {option.name}.')
            seen.add(key)
            if rate.duration_minutes != option.duration_minutes or rate.min_guests != option.min_guests or rate.max_guests != option.max_guests:
                issues.append(f'Match the rate duration and party limits to {option.name}.')
    if google:
        if tour.status != 'PUBLISHED' or not tour.is_active or not tour.google_activity_enabled:
            issues.append('Enable Google activity distribution for a published activity.')
        if not tour.external_booking_url.startswith('https://'):
            issues.append('Confirm a channel-compatible booking path; an enquiry page alone is not assumed eligible.')
        if primary:
            scale = min(1, 1280 / max(primary.width, primary.height)) if primary.width and primary.height and primary.webp_image else 1
            google_width, google_height = int(primary.width * scale), int(primary.height * scale)
            if not primary.google_activity_eligible or not (300 <= google_width <= 4000 and 300 <= google_height <= 4000):
                issues.append('Check primary Google image eligibility and dimensions.')
            if primary.content_hash and type(primary).objects.filter(is_primary=True, content_hash=primary.content_hash).exclude(tour=tour).exists():
                issues.append('Use a unique primary image for this activity.')
        standard = tour.current_rates.filter(audience_type__in=['ALL', 'NON_RESIDENT'], verified_at__isnull=False)
        if not standard.exists():
            issues.append('Configure a verified standard adult rate for channel submission.')
        for rate in standard:
            quote = quote_activity(tour, adults=rate.min_guests, option_id=rate.option_id,
                currency=rate.currency, visitor_type='NON_RESIDENT', service_date=timezone.localdate())
            if not quote.complete:
                issues.append(f'Confirm the mandatory-fee total for {rate.name}.')
    return list(dict.fromkeys(issues))
