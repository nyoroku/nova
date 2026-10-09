from urllib.parse import urlparse
from .models import SiteSettings
from django.conf import settings
import json

def nova_site_context(request):
    """
    Supplies the singleton SiteSettings, sanitized canonical URL,
    and brand identity tokens to all Django templates.
    """
    settings_obj = SiteSettings.get_solo()
    
    # Strip query parameters for canonical URL
    parsed = urlparse(request.build_absolute_uri(request.path))
    clean_canonical = settings.SITE_URL.rstrip('/') + parsed.path
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'LocalBusiness', '@id': settings.SITE_URL + '/#business', 'name': settings_obj.business_name,
         'description': settings_obj.supporting_proposition, 'telephone': settings_obj.phone_e164,
         'email': settings_obj.email, 'url': settings.SITE_URL + '/',
         'address': {'@type': 'PostalAddress', 'streetAddress': settings_obj.street_address,
                     'addressLocality': settings_obj.locality, 'addressRegion': settings_obj.county, 'addressCountry': 'KE'}},
        {'@type': 'WebSite', '@id': settings.SITE_URL + '/#website', 'url': settings.SITE_URL + '/', 'name':settings_obj.business_name},
        {'@type': 'WebPage', '@id': clean_canonical + '#webpage', 'url': clean_canonical} ]}
    
    return {
        'site_settings': settings_obj,
        'canonical_url': clean_canonical,
        'site_origin': settings.SITE_URL,
        'activity_asset_version': settings.NOVA_ASSET_VERSION,
        'business_schema': json.dumps(graph).replace('<', '\\u003c'),
        'brand': {
            'name': settings_obj.business_name,
            'tagline': settings_obj.tagline,
            'whatsapp_url': f"https://wa.me/{settings_obj.whatsapp_number}",
            'phone_display': settings_obj.phone_display,
            'email': settings_obj.email,
        }
    }
