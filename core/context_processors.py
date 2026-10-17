from urllib.parse import urlparse
from .models import SiteSettings
from django.conf import settings
import json

HUB_LABELS = {
    '/boat-rides/': 'Boat Rides',
    '/prices/': 'Prices',
    '/services/': 'Services',
    '/hotel-boat-rides/': 'Hotel Departures',
    '/questions/': 'Questions & FAQs',
    '/contact/': 'Contact & Directions',
    '/about/': 'About Nova',
    '/plan-naivasha/': 'Plan Naivasha',
    '/stay/': 'Stay by the Lake',
    '/packages/': 'Packages',
    '/book/': 'Book / Enquire',
    '/journal/': "Captain's Journal",
}

def nova_site_context(request):
    """
    Supplies the singleton SiteSettings, sanitized canonical URL,
    and brand identity tokens to all Django templates.
    """
    settings_obj = SiteSettings.get_solo()
    attr = getattr(request, 'nova_attribution', None) or {}
    
    # Strip query parameters for canonical URL
    parsed = urlparse(request.build_absolute_uri(request.path))
    clean_canonical = settings.SITE_URL.rstrip('/') + parsed.path

    business_node = {
        '@type': 'LocalBusiness',
        '@id': settings.SITE_URL + '/#business',
        'name': settings_obj.business_name,
        'legalName': settings_obj.legal_name,
        'description': settings_obj.supporting_proposition,
        'telephone': settings_obj.phone_e164,
        'email': settings_obj.email,
        'url': settings.SITE_URL + '/',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': settings_obj.street_address,
            'addressLocality': settings_obj.locality,
            'addressRegion': settings_obj.county,
            'addressCountry': 'KE',
        },
        'geo': {
            '@type': 'GeoCoordinates',
            'latitude': float(settings_obj.standard_launch_lat),
            'longitude': float(settings_obj.standard_launch_lng),
        },
        'openingHoursSpecification': {
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': [
                'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday',
            ],
            'opens': settings_obj.opening_time.strftime('%H:%M') if hasattr(settings_obj.opening_time, 'strftime') else str(settings_obj.opening_time)[:5],
            'closes': settings_obj.closing_time.strftime('%H:%M') if hasattr(settings_obj.closing_time, 'strftime') else str(settings_obj.closing_time)[:5],
        },
    }
    raw_same_as = settings_obj.same_as_urls or []
    same_as = (
        [str(u).strip() for u in raw_same_as if str(u).strip()]
        if isinstance(raw_same_as, list)
        else [u.strip() for u in str(raw_same_as).splitlines() if u.strip()]
    )
    if same_as:
        business_node['sameAs'] = same_as

    graph_nodes = [
        business_node,
        {'@type': 'WebSite', '@id': settings.SITE_URL + '/#website', 'url': settings.SITE_URL + '/', 'name': settings_obj.business_name},
        {'@type': 'WebPage', '@id': clean_canonical + '#webpage', 'url': clean_canonical},
    ]

    if parsed.path in HUB_LABELS:
        graph_nodes.append({
            '@type': 'BreadcrumbList',
            '@id': clean_canonical + '#breadcrumb',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': settings.SITE_URL + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': HUB_LABELS[parsed.path], 'item': clean_canonical},
            ],
        })

    graph = {'@context': 'https://schema.org', '@graph': graph_nodes}
    
    return {
        'site_settings': settings_obj,
        'canonical_url': clean_canonical,
        'site_origin': settings.SITE_URL,
        'activity_asset_version': settings.NOVA_ASSET_VERSION,
        'business_schema': json.dumps(graph).replace('<', '\\u003c'),
        'attribution': attr,
        'brand': {
            'name': settings_obj.business_name,
            'tagline': settings_obj.tagline,
            'whatsapp_url': f"https://wa.me/{settings_obj.whatsapp_number}",
            'phone_display': settings_obj.phone_display,
            'email': settings_obj.email,
        }
    }

