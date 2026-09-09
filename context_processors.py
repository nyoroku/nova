from django.conf import settings

def site_config(request):
    whatsapp_number = settings.SITE_WHATSAPP_NUMBER
    canonical_url = request.build_absolute_uri(request.path)
    return {
        'site_config': {
            'name': settings.SITE_NAME,
            'short_name': settings.SITE_SHORT_NAME,
            'domain': settings.SITE_DOMAIN,
            'url': settings.SITE_URL,
            'phone_display': settings.SITE_PHONE_DISPLAY,
            'phone_e164': settings.SITE_PHONE_E164,
            'whatsapp_number': whatsapp_number,
            'whatsapp_url': f'https://wa.me/{whatsapp_number}',
            'email': settings.SITE_EMAIL,
        },
        'canonical_url': canonical_url,
    }
