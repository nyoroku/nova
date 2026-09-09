from urllib.parse import urlparse
from .models import SiteSettings

def nova_site_context(request):
    """
    Supplies the singleton SiteSettings, sanitized canonical URL,
    and brand identity tokens to all Django templates.
    """
    settings_obj = SiteSettings.get_solo()
    
    # Strip query parameters for canonical URL
    parsed = urlparse(request.build_absolute_uri(request.path))
    clean_canonical = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    return {
        'site_settings': settings_obj,
        'canonical_url': clean_canonical,
        'brand': {
            'name': settings_obj.business_name,
            'tagline': settings_obj.tagline,
            'whatsapp_url': f"https://wa.me/{settings_obj.whatsapp_number}",
            'phone_display': settings_obj.phone_display,
            'email': settings_obj.email,
        }
    }
