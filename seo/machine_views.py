import hashlib
import json
import re
from datetime import datetime, time
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotModified
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import http_date

from core.models import SiteSettings, BusinessFact, ClaimEvidence, ExternalFee
from tours.models import Tour, GBPService, ServiceIntent
from tours.pricing import valid_on
from partners.models import HotelAccess
from content.models import GuideArticle, QuestionAnswer


def _latest_timestamp(*dates):
    valid_dates = []
    for d in dates:
        if not d:
            continue
        if isinstance(d, datetime):
            valid_dates.append(d)
        else:
            valid_dates.append(timezone.make_aware(datetime.combine(d, time(12, 0))))
    if not valid_dates:
        return timezone.now()
    return max(valid_dates)


def _machine_response(request, content: str, content_type: str, last_modified_dt=None):
    body_bytes = force_bytes(content)
    etag = f'"{hashlib.sha256(body_bytes).hexdigest()[:24]}"'
    if request.META.get('HTTP_IF_NONE_MATCH') == etag:
        not_modified = HttpResponseNotModified()
        not_modified['ETag'] = etag
        not_modified['Cache-Control'] = 'public, max-age=300, must-revalidate'
        return not_modified

    response = HttpResponse(body_bytes, content_type=content_type)
    response['ETag'] = etag
    response['Cache-Control'] = 'public, max-age=300, must-revalidate'
    response['X-Robots-Tag'] = 'index, follow'
    if last_modified_dt:
        response['Last-Modified'] = http_date(last_modified_dt.timestamp())
    return response


def _html_to_markdown(html_text: str) -> str:
    if not html_text:
        return ''
    text = html_text
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: f"\n\n## {strip_tags(m.group(1)).strip()}\n\n", text, flags=re.I | re.S)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f"\n\n### {strip_tags(m.group(1)).strip()}\n\n", text, flags=re.I | re.S)
    text = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"- {strip_tags(m.group(1)).strip()}\n", text, flags=re.I | re.S)
    text = re.sub(r'</p>', '\n\n', text, flags=re.I)
    text = strip_tags(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def serialize_activity(tour: Tour) -> dict:
    config = SiteSettings.get_solo()
    options_qs = tour.options.filter(is_active=True).prefetch_related('external_fees')
    rates_qs = tour.current_rates
    fees_qs = valid_on(ExternalFee.objects.filter(touroption__tour=tour).distinct(), timezone.localdate())

    options_data = [
        {
            'id': opt.pk,
            'name': opt.name,
            'mode': opt.mode,
            'mode_display': opt.get_mode_display(),
            'duration_minutes': opt.duration_minutes,
            'min_guests': opt.min_guests,
            'max_guests': opt.max_guests,
            'verified_at': str(opt.verified_at) if opt.verified_at else None,
        }
        for opt in options_qs
    ]

    rates_data = [
        {
            'name': r.name,
            'option_name': r.option.name if r.option else '',
            'pricing_model': r.pricing_model,
            'unit_label': r.unit_label,
            'currency': r.currency,
            'amount': str(r.amount) if r.has_exact_price else None,
            'minimum_total': str(r.minimum_total) if r.minimum_total is not None else None,
            'audience_type': r.audience_type,
            'audience_display': r.get_audience_type_display(),
            'duration_minutes': r.option.duration_minutes if r.option else r.duration_minutes,
            'min_guests': r.min_guests,
            'max_guests': r.max_guests,
            'verified_at': str(r.verified_at) if r.verified_at else str(r.effective_from),
        }
        for r in rates_qs
    ]

    fees_data = [
        {
            'provider_name': f.provider_name,
            'service_name': f.service_name,
            'visitor_type': f.visitor_type,
            'visitor_type_display': f.get_visitor_type_display(),
            'currency': f.currency,
            'adult_amount': str(f.adult_amount),
            'child_amount': str(f.child_amount) if f.child_amount is not None else None,
            'disclaimer': f.disclaimer,
            'last_verified_at': str(f.last_verified_at),
        }
        for f in fees_qs
    ]

    start_rate = tour.starting_rate
    duration_min = start_rate.option.duration_minutes if start_rate and start_rate.option else tour.duration_minutes

    return {
        'name': tour.name,
        'branded_name': tour.effective_branded_name,
        'gbp_activity_name': tour.effective_gbp_activity_name,
        'slug': tour.slug,
        'canonical_url': tour.canonical_url,
        'gbp_booking_url': tour.gbp_booking_url,
        'category': tour.get_category_display(),
        'primary_intent': tour.primary_intent or tour.name.lower(),
        'audience_tags': [t.strip() for t in tour.audience_tags.split(',') if t.strip()],
        'short_answer': tour.short_answer,
        'direct_answer': tour.direct_answer or tour.summary,
        'summary': tour.summary,
        'duration_minutes': duration_min,
        'public_duration_display': tour.public_duration_display,
        'options': options_data,
        'rates': rates_data,
        'inclusions': tour.inclusion_items,
        'exclusions': tour.exclusion_items,
        'external_fees': fees_data,
        'departure_point': tour.meeting_point or config.standard_launch_name,
        'arrival_minutes_before': tour.arrival_minutes_before,
        'best_for': tour.best_for,
        'safety_briefing': tour.safety_briefing,
        'weather_policy': tour.weather_policy,
        'cancellation_policy': tour.cancellation_policy,
        'booking_urls': {
            'web': f"{settings.SITE_URL}{tour.enquiry_url}",
            'whatsapp': tour.whatsapp_url,
            'gbp': tour.gbp_booking_url,
        },
        'machine_urls': {
            'json': f"{settings.SITE_URL}/activities/{tour.slug}.json",
            'markdown': f"{settings.SITE_URL}/activities/{tour.slug}.md",
        },
        'faqs': [
            {'question': faq.question, 'answer': faq.answer}
            for faq in tour.faqs.all()
        ],
        'last_verified_at': str(tour.last_verified_at),
    }


def llms_txt(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().prefetch_related('rates__option').order_by('order'))
    facts = {f.key: f for f in BusinessFact.objects.filter(active=True)}
    latest_dt = _latest_timestamp(
        *[t.updated_at for t in tours],
        *[f.last_verified_at for f in facts.values()],
    )

    lines = [
        f"# {config.business_name}",
        "",
        f"> {config.business_name} ({config.tagline} — {config.supporting_proposition}) is a licensed boat ride and lake safari operator on Lake Naivasha, Kenya. Departures operate daily ({config.operating_hours}) from {config.standard_launch_name} on Moi South Lake Road ({config.standard_launch_lat}, {config.standard_launch_lng}) and from operationally verified Lake Naivasha hotel jetties. Direct booking and enquiries via WhatsApp or phone at {config.phone_display} ({config.phone_e164}).",
        "",
        "## Core Commercial Hubs",
        "",
        f"- [Boat Rides & Activities Hub]({settings.SITE_URL}/boat-rides/): Full catalogue of guided Lake Naivasha boat rides, wildlife safaris, and Crescent Island transfers ([Markdown]({settings.SITE_URL}/boat-rides.md))",
        f"- [Boat Ride Prices & Rate Card]({settings.SITE_URL}/prices/): Active public rates per boat and per person, inclusions, Crescent Island entry fees, and hotel departure fees ([Markdown]({settings.SITE_URL}/prices.md))",
        f"- [Lake Naivasha Boat & Tour Services]({settings.SITE_URL}/services/): 16 canonical Google Business Profile services and 30 search intents mapped to bookable experiences ([Markdown]({settings.SITE_URL}/services.md))",
        f"- [Hotel Jetty Departures & Pickup Checker]({settings.SITE_URL}/hotel-boat-rides/): Verified hotel jetty boarding, positioning fees, and road transfer logistics ([Markdown]({settings.SITE_URL}/hotel-boat-rides.md))",
        f"- [Frequently Asked Questions]({settings.SITE_URL}/questions/): Direct answers on prices, timing, safety, children, and Crescent Island rules ([Markdown]({settings.SITE_URL}/questions.md))",
        f"- [Contact & Launch Base Directions]({settings.SITE_URL}/contact/): GPS coordinates, driving directions from Nairobi/Naivasha, and WhatsApp dispatch desk",
        "",
        "## Bookable Lake Naivasha Activities",
        "",
    ]

    for tour in tours:
        rate = tour.starting_rate
        rate_str = (
            f"From {rate.currency} {rate.amount:g} {rate.unit_label}"
            if rate and rate.has_exact_price
            else "Custom quote on request"
        )
        lines.append(
            f"- [{tour.name} ({tour.effective_branded_name})]({tour.canonical_url}): "
            f"{tour.public_duration_display} · {rate_str}. {tour.short_answer} "
            f"([Markdown]({settings.SITE_URL}/activities/{tour.slug}.md) | [JSON]({settings.SITE_URL}/activities/{tour.slug}.json))"
        )

    lines.extend([
        "",
        "## Machine & Agent Discovery Endpoints",
        "",
        f"- [Expanded Knowledge & Rate Reference (/llms-full.txt)]({settings.SITE_URL}/llms-full.txt)",
        f"- [Structured Activity Catalogue (/activities/index.json)]({settings.SITE_URL}/activities/index.json)",
        f"- [AI Discovery Catalog (/.well-known/ai-catalog.json)]({settings.SITE_URL}/.well-known/ai-catalog.json)",
        f"- [XML Sitemap (/sitemap.xml)]({settings.SITE_URL}/sitemap.xml)",
        "",
    ])

    return _machine_response(request, "\n".join(lines), 'text/plain; charset=utf-8', latest_dt)


def llms_full_txt(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().prefetch_related('rates__option', 'faqs', 'itinerary_steps').order_by('order'))
    facts = list(BusinessFact.objects.filter(active=True).order_by('key'))
    claims = list(ClaimEvidence.objects.filter(publishable=True).order_by('claim_key'))
    gbp_services = list(GBPService.objects.filter(is_active=True).select_related('activity').order_by('number', 'name'))
    external_fees = list(valid_on(ExternalFee.objects.all(), timezone.localdate()).order_by('provider_name', 'visitor_type'))
    hotel_accesses = list(HotelAccess.objects.filter(is_published=True).select_related('property').order_by('property__order', 'property__name'))
    faqs = list(QuestionAnswer.objects.filter(is_active=True).order_by('order'))

    latest_dt = _latest_timestamp(
        *[t.updated_at for t in tours],
        *[f.last_verified_at for f in facts],
    )

    lines = [
        f"# {config.business_name} — Canonical Full Reference (llms-full.txt)",
        "",
        f"Canonical Website: {settings.SITE_URL}/",
        f"Last Generated: {timezone.localdate().isoformat()}",
        "",
        "## 1. Canonical Business Facts",
        "",
        "| Fact | Value | Last Verified | Source |",
        "|---|---|---|---|",
    ]
    for f in facts:
        lines.append(f"| {f.public_label} | {f.value} | {f.last_verified_at} | {f.verification_source} |")

    if claims:
        lines.extend([
            "",
            "## 2. Verified Operational & Safety Claims",
            "",
        ])
        for c in claims:
            lines.append(f"- **{c.claim_key}** ({c.get_evidence_type_display()}, verified {c.verified_at}): {c.claim_text}")

    lines.extend([
        "",
        "## 3. Published Lake Naivasha Activities & Rates",
        "",
    ])
    for tour in tours:
        lines.extend([
            f"### {tour.name} ({tour.effective_branded_name})",
            f"- **Canonical URL**: {tour.canonical_url}",
            f"- **Machine JSON**: {settings.SITE_URL}/activities/{tour.slug}.json",
            f"- **Machine Markdown**: {settings.SITE_URL}/activities/{tour.slug}.md",
            f"- **Category**: {tour.get_category_display()}",
            f"- **Duration**: {tour.public_duration_display}",
            f"- **Departure Point**: {tour.meeting_point} (arrive {tour.arrival_minutes_before} mins early)",
            f"- **Last Verified**: {tour.last_verified_at}",
            "",
            f"**Direct Answer**: {tour.direct_answer or tour.summary}",
            "",
            "**Active Rates**:",
        ])
        for r in tour.current_rates:
            price_txt = f"{r.currency} {r.amount:g} {r.unit_label}" if r.has_exact_price else "Request custom quote"
            lines.append(
                f"- {r.option.name if r.option else r.name}: {price_txt} "
                f"({r.option.duration_minutes if r.option else r.duration_minutes} mins, "
                f"{r.min_guests}–{r.max_guests} guests, {r.get_audience_type_display()}, verified {r.verified_at or r.effective_from})"
            )
        lines.append("")
        lines.append("**Included**: " + "; ".join(tour.inclusion_items))
        lines.append("**Excluded**: " + "; ".join(tour.exclusion_items))
        lines.append("")

    lines.extend([
        "## 4. Canonical Google Business Profile Services (16)",
        "",
        "| Category | Service Name | Description | Destination |",
        "|---|---|---|---|",
    ])
    for gs in gbp_services:
        lines.append(f"| {gs.gbp_category_name} | {gs.service_name} | {gs.short_description} | {settings.SITE_URL}{gs.destination} |")

    lines.extend([
        "",
        "## 5. Separate Attraction Admission Fees",
        "",
        "| Attraction | Visitor Category | Adult | Child | Last Verified |",
        "|---|---|---|---|---|",
    ])
    for fee in external_fees:
        child_str = f"{fee.currency} {fee.child_amount:g}" if fee.child_amount is not None else "Confirm eligibility"
        lines.append(
            f"| {fee.provider_name} ({fee.service_name}) | {fee.get_visitor_type_display()} | "
            f"{fee.currency} {fee.adult_amount:g} | {child_str} | {fee.last_verified_at} |"
        )

    lines.extend([
        "",
        "## 6. Hotel Departure Access & Positioning",
        "",
        "| Property | Access Status | Positioning Fee | Advance Notice | Last Verified |",
        "|---|---|---|---|---|",
    ])
    for access in hotel_accesses:
        pos_str = (
            f"{access.currency} {access.positioning_fee:g} per boat"
            if access.is_operationally_verified
            else "Request confirmed quote"
        )
        lines.append(
            f"| {access.property.name} | {access.public_access_label} | {pos_str} | "
            f"{access.advance_notice_hours}h | {access.last_verified_at or 'Ask Nova'} |"
        )

    lines.extend([
        "",
        "## 7. Frequently Asked Questions",
        "",
    ])
    for faq in faqs:
        ans = faq.plain_answer or strip_tags(faq.answer)
        lines.extend([
            f"### {faq.question}",
            ans.strip(),
            "",
        ])

    return _machine_response(request, "\n".join(lines), 'text/plain; charset=utf-8', latest_dt)


def activities_index_json(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().prefetch_related('rates__option', 'options__external_fees', 'faqs').order_by('order'))
    latest_dt = _latest_timestamp(*[t.updated_at for t in tours])
    payload = {
        'business': {
            'name': config.business_name,
            'legal_name': config.legal_name,
            'url': f"{settings.SITE_URL}/",
            'phone_display': config.phone_display,
            'phone_e164': config.phone_e164,
            'whatsapp_url': f"https://wa.me/{config.whatsapp_number}",
            'operating_hours': config.operating_hours,
            'launch_base': config.standard_launch_name,
            'coordinates': {
                'latitude': float(config.standard_launch_lat),
                'longitude': float(config.standard_launch_lng),
            },
        },
        'generated_at': timezone.localdate().isoformat(),
        'count': len(tours),
        'activities': [serialize_activity(t) for t in tours],
    }
    return _machine_response(
        request,
        json.dumps(payload, indent=2, ensure_ascii=False),
        'application/json; charset=utf-8',
        latest_dt,
    )


def activity_detail_json(request, slug):
    tour = get_object_or_404(
        Tour.objects.published().prefetch_related('rates__option', 'options__external_fees', 'faqs'),
        slug=slug,
    )
    payload = serialize_activity(tour)
    return _machine_response(
        request,
        json.dumps(payload, indent=2, ensure_ascii=False),
        'application/json; charset=utf-8',
        tour.updated_at,
    )


def activity_detail_md(request, slug):
    config = SiteSettings.get_solo()
    tour = get_object_or_404(
        Tour.objects.published().prefetch_related('rates__option', 'options__external_fees', 'faqs', 'itinerary_steps', 'details'),
        slug=slug,
    )
    data = serialize_activity(tour)
    start_rate = tour.starting_rate
    start_rate_str = (
        f"From {start_rate.currency} {start_rate.amount:g} {start_rate.unit_label}"
        if start_rate and start_rate.has_exact_price
        else "Custom quote on request"
    )

    lines = [
        f"# {tour.name} ({tour.effective_branded_name})",
        "",
        f"**Category**: {data['category']}  ",
        f"**Canonical URL**: {tour.canonical_url}  ",
        f"**Last Verified**: {data['last_verified_at']}  ",
        "",
        f"> {data['direct_answer']}",
        "",
        "## At a Glance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Experience Name | {tour.name} ({tour.effective_branded_name}) |",
        f"| Duration | {tour.public_duration_display} |",
        f"| Starting Rate | {start_rate_str} |",
        f"| Departure Point | {data['departure_point']} (arrive {tour.arrival_minutes_before} mins before departure) |",
        f"| Best Suited For | {tour.best_for or 'Families, couples, groups & wildlife travellers'} |",
        f"| Last Verified | {data['last_verified_at']} |",
        "",
        "## Active Rates & Options",
        "",
        "| Option | Duration | Guests | Price | Visitor Category | Last Verified |",
        "|---|---|---|---|---|---|",
    ]
    for r in data['rates']:
        price_col = f"{r['currency']} {r['amount']} {r['unit_label']}" if r['amount'] else "Request individual quote"
        lines.append(
            f"| {r['option_name'] or r['name']} | {r['duration_minutes']} mins | "
            f"{r['min_guests']}–{r['max_guests']} | {price_col} | {r['audience_display']} | {r['verified_at']} |"
        )

    lines.extend([
        "",
        "## Included & Excluded",
        "",
        "### Included",
    ])
    for item in data['inclusions']:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "### Not Included",
    ])
    for item in data['exclusions']:
        lines.append(f"- {item}")

    if data['external_fees']:
        lines.extend([
            "",
            "## Mandatory External Attraction Fees",
            "",
            "| Attraction / Category | Adult | Child | Last Verified |",
            "|---|---|---|---|",
        ])
        for f in data['external_fees']:
            child_col = f"{f['currency']} {f['child_amount']}" if f['child_amount'] else "Confirm eligibility"
            lines.append(
                f"| {f['provider_name']} · {f['visitor_type_display']} | "
                f"{f['currency']} {f['adult_amount']} | {child_col} | {f['last_verified_at']} |"
            )

    steps = list(tour.itinerary_steps.all())
    if steps:
        lines.extend([
            "",
            "## Typical Itinerary",
            "",
        ])
        for idx, step in enumerate(steps, 1):
            lines.append(f"{idx}. **{step.title}**: {step.description}")

    lines.extend([
        "",
        "## Experience Overview",
        "",
        tour.body.strip(),
        "",
        "## Safety, Weather & Cancellation Policies",
        "",
        f"- **Safety & Children**: {tour.safety_briefing} {tour.child_policy}",
        f"- **Accessibility**: {tour.accessibility_notes}",
        f"- **Weather Policy**: {tour.weather_policy}",
        f"- **Cancellation Policy**: {tour.cancellation_policy}",
    ])

    if data['faqs']:
        lines.extend([
            "",
            "## Frequently Asked Questions",
            "",
        ])
        for faq in data['faqs']:
            lines.extend([
                f"### {faq['question']}",
                faq['answer'],
                "",
            ])

    lines.extend([
        "",
        "## Book or Enquire",
        "",
        f"- **Web Enquiry**: {data['booking_urls']['web']}",
        f"- **WhatsApp Dispatch ({config.phone_display})**: {data['booking_urls']['whatsapp']}",
        f"- **Structured JSON**: {data['machine_urls']['json']}",
        "",
    ])

    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', tour.updated_at)


def boat_rides_hub_md(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().prefetch_related('rates__option').order_by('order'))
    latest_dt = _latest_timestamp(*[t.updated_at for t in tours])

    lines = [
        "# Lake Naivasha Boat Rides & Safaris — Nova Boat Rides Naivasha",
        "",
        f"**Canonical URL**: {settings.SITE_URL}/boat-rides/  ",
        f"**Launch Base**: {config.standard_launch_name} ({config.standard_launch_lat}, {config.standard_launch_lng})  ",
        f"**Operating Hours**: {config.operating_hours}  ",
        f"**WhatsApp / Phone**: {config.phone_display} ({config.phone_e164})  ",
        "",
        "> Nova Boat Rides Naivasha operates private and shared boat rides, hippo and birdwatching safaris, Crescent Island boat transfers, sunset cruises, family rides, bird photography charters, and group outings on Lake Naivasha.",
        "",
        "## Published Activities",
        "",
        "| Activity | Branded Name | Duration | Starting Rate | Canonical URL |",
        "|---|---|---|---|---|",
    ]
    for tour in tours:
        rate = tour.starting_rate
        rate_str = f"From {rate.currency} {rate.amount:g} {rate.unit_label}" if rate and rate.has_exact_price else "Request quote"
        lines.append(
            f"| {tour.name} | {tour.effective_branded_name} | {tour.public_duration_display} | "
            f"{rate_str} | {tour.canonical_url} |"
        )
    lines.append("")
    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def prices_hub_md(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().prefetch_related('rates__option').order_by('order'))
    external_fees = list(valid_on(ExternalFee.objects.all(), timezone.localdate()).order_by('provider_name', 'visitor_type'))
    hotel_accesses = list(HotelAccess.objects.filter(is_published=True).select_related('property').order_by('property__order', 'property__name'))
    latest_dt = _latest_timestamp(*[t.updated_at for t in tours])

    lines = [
        "# Lake Naivasha Boat Ride Prices & Booking Options — Nova",
        "",
        f"**Canonical URL**: {settings.SITE_URL}/prices/  ",
        f"**Last Verified**: {timezone.localdate().isoformat()}  ",
        "",
        "> Private boat prices cover the stated party limit; shared-seat prices apply per person. Attraction admission, hotel boat positioning, and road transfers are quoted separately where required.",
        "",
        "## Active Public Boat Ride Rates",
        "",
        "| Experience | Option | Duration | Guests | Price | Visitor Category | Last Verified |",
        "|---|---|---|---|---|---|---|",
    ]
    for tour in tours:
        for r in tour.current_rates:
            p_str = f"{r.currency} {r.amount:g} {r.unit_label}" if r.has_exact_price else "Request individual quote"
            lines.append(
                f"| [{tour.name}]({tour.canonical_url}) | {r.option.name if r.option else r.name} | "
                f"{r.option.duration_minutes if r.option else r.duration_minutes} mins | "
                f"{r.min_guests}–{r.max_guests} | {p_str} | {r.get_audience_type_display()} | "
                f"{r.verified_at or r.effective_from} |"
            )

    lines.extend([
        "",
        "## Included in Boat Rates",
        f"- Licensed Lake Naivasha boat and certified Nova captain",
        f"- Safety briefing and fitted life jackets for all passengers",
        f"- Boat fuel for the confirmed duration and route",
        f"- Standard boarding at {config.standard_launch_name}",
        "",
        "## Excluded / Quoted Separately",
        "- Crescent Island Game Sanctuary entry fees (per person, by residency category)",
        "- Hotel jetty boat positioning fees or road transfers where applicable",
        "- Meals, refreshments, personal insurance, and optional crew gratuities",
        "",
        "## Mandatory Attraction Fees",
        "",
        "| Attraction / Category | Adult | Child | Last Verified |",
        "|---|---|---|---|",
    ])
    for fee in external_fees:
        c_str = f"{fee.currency} {fee.child_amount:g}" if fee.child_amount is not None else "Confirm eligibility"
        lines.append(
            f"| {fee.provider_name} · {fee.get_visitor_type_display()} | "
            f"{fee.currency} {fee.adult_amount:g} | {c_str} | {fee.last_verified_at} |"
        )

    lines.extend([
        "",
        "## Hotel Departure Charges",
        "",
        "| Property | Access Status | Positioning Fee | Notice / Last Checked |",
        "|---|---|---|---|",
    ])
    for access in hotel_accesses:
        p_col = (
            f"{access.currency} {access.positioning_fee:g} per boat"
            if access.is_operationally_verified
            else "Request confirmed quote"
        )
        lines.append(
            f"| {access.property.name} | {access.public_access_label} | {p_col} | "
            f"{access.advance_notice_hours}h · {access.last_verified_at or 'Ask Nova'} |"
        )
    lines.append("")
    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def services_hub_md(request):
    gbp_services = list(GBPService.objects.filter(is_active=True).select_related('activity').order_by('number', 'name'))
    intents = list(ServiceIntent.objects.filter(is_active=True).select_related('activity').order_by('level', 'name'))
    latest_dt = _latest_timestamp(*[gs.last_verified_at for gs in gbp_services])

    lines = [
        "# Boat Ride & Tour Services in Naivasha — Nova",
        "",
        f"**Canonical URL**: {settings.SITE_URL}/services/  ",
        "",
        "## Core Lake Naivasha Services (16 Canonical GBP Services)",
        "",
        "| Category | Service Name | Description | Destination |",
        "|---|---|---|---|",
    ]
    for gs in gbp_services:
        lines.append(
            f"| {gs.gbp_category_name} | {gs.service_name} | {gs.short_description} | {settings.SITE_URL}{gs.destination} |"
        )

    lines.extend([
        "",
        "## Search Intent Directory (30 Services)",
        "",
        "| Service | Level | Destination |",
        "|---|---|---|",
    ])
    for intent in intents:
        lines.append(f"| {intent.name} | {intent.level} | {settings.SITE_URL}{intent.destination} |")
    lines.append("")
    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def questions_hub_md(request):
    faqs = list(QuestionAnswer.objects.filter(is_active=True).order_by('order'))
    latest_dt = _latest_timestamp(*[f.verified_at for f in faqs])

    lines = [
        "# Lake Naivasha Boat Ride FAQs & Direct Answers — Nova",
        "",
        f"**Canonical URL**: {settings.SITE_URL}/questions/  ",
        "",
    ]
    for faq in faqs:
        ans = faq.plain_answer or strip_tags(faq.answer)
        lines.extend([
            f"## {faq.question}",
            "",
            ans.strip(),
            "",
        ])
    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def hotel_hub_md(request):
    config = SiteSettings.get_solo()
    accesses = list(HotelAccess.objects.filter(is_published=True).select_related('property').order_by('property__order', 'property__name'))
    latest_dt = _latest_timestamp(*[a.last_verified_at for a in accesses])

    lines = [
        "# Lake Naivasha Boat Rides from Your Hotel — Nova Hotel Departures",
        "",
        f"**Canonical URL**: {settings.SITE_URL}/hotel-boat-rides/  ",
        f"**Standard Launch Base**: {config.standard_launch_name} ({config.standard_launch_lat}, {config.standard_launch_lng})  ",
        "",
        "> Nova coordinates boat departures from verified lakeside hotel jetties where water depth and property permissions allow, or arranges road transfers to Nova Karagita Base.",
        "",
        "## Hotel Departure Verification Matrix",
        "",
        "| Property | Area | Access Status | Positioning Fee | Advance Notice | Last Verified |",
        "|---|---|---|---|---|---|",
    ]
    for a in accesses:
        fee_str = (
            f"{a.currency} {a.positioning_fee:g} per boat"
            if a.is_operationally_verified
            else "Request confirmed quote"
        )
        lines.append(
            f"| {a.property.name} | {a.property.location_area} | {a.public_access_label} | "
            f"{fee_str} | {a.advance_notice_hours}h | {a.last_verified_at or 'Ask Nova'} |"
        )
    lines.append("")
    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def journal_detail_md(request, slug):
    article = get_object_or_404(
        GuideArticle.objects.select_related('related_activity'),
        slug=slug,
        is_active=True,
    )
    target = article.target_activity
    tours = list(Tour.objects.published().prefetch_related('rates__option').order_by('order')[:6])
    latest_dt = _latest_timestamp(article.updated_at, article.verified_at)

    lines = [
        f"# {article.title}",
        "",
        f"**Canonical URL**: {settings.SITE_URL}{article.get_absolute_url()}  ",
        f"**Author**: {article.author_captain.name if article.author_captain else article.author}  ",
        f"**Category**: {article.get_category_display()}  ",
        f"**Last Verified**: {article.verified_at or article.updated_at.date()}  ",
        "",
    ]
    if article.direct_quick_answer:
        lines.extend([
            "## Quick Answer",
            "",
            f"> {article.direct_quick_answer}",
            "",
        ])

    lines.extend([
        _html_to_markdown(article.body),
        "",
        "## Live Canonical Boat Ride Rates",
        "",
        "| Activity | Duration | Starting Rate | URL |",
        "|---|---|---|---|",
    ])
    for t in tours:
        r = t.starting_rate
        r_str = f"From {r.currency} {r.amount:g} {r.unit_label}" if r and r.has_exact_price else "Request quote"
        lines.append(f"| {t.name} | {t.public_duration_display} | {r_str} | {t.canonical_url} |")

    if target:
        lines.extend([
            "",
            "## Recommended Next Step",
            "",
            f"- **[{target.name}]({target.canonical_url})**: {target.short_answer}",
            f"- **Enquire / Check Availability**: {settings.SITE_URL}{target.enquiry_url}",
            "",
        ])

    return _machine_response(request, "\n".join(lines), 'text/markdown; charset=utf-8', latest_dt)


def ai_catalog_json(request):
    config = SiteSettings.get_solo()
    tours = list(Tour.objects.published().order_by('order'))
    latest_dt = _latest_timestamp(*[t.updated_at for t in tours])
    payload = {
        'schema_version': '1.0',
        'business_name': config.business_name,
        'site_url': f"{settings.SITE_URL}/",
        'llms_txt': f"{settings.SITE_URL}/llms.txt",
        'llms_full_txt': f"{settings.SITE_URL}/llms-full.txt",
        'activities_index_json': f"{settings.SITE_URL}/activities/index.json",
        'sitemap_xml': f"{settings.SITE_URL}/sitemap.xml",
        'hubs_markdown': {
            'boat_rides': f"{settings.SITE_URL}/boat-rides.md",
            'prices': f"{settings.SITE_URL}/prices.md",
            'services': f"{settings.SITE_URL}/services.md",
            'questions': f"{settings.SITE_URL}/questions.md",
            'hotel_departures': f"{settings.SITE_URL}/hotel-boat-rides.md",
        },
        'activities': [
            {
                'slug': t.slug,
                'name': t.name,
                'branded_name': t.effective_branded_name,
                'html_url': t.canonical_url,
                'json_url': f"{settings.SITE_URL}/activities/{t.slug}.json",
                'markdown_url': f"{settings.SITE_URL}/activities/{t.slug}.md",
            }
            for t in tours
        ],
    }
    return _machine_response(
        request,
        json.dumps(payload, indent=2, ensure_ascii=False),
        'application/json; charset=utf-8',
        latest_dt,
    )
