from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

CAMPAIGNS = {'profile': 'gbp_profile', 'activity': 'gbp_activities', 'post': 'gbp_posts', 'things_to_do': 'things_to_do'}
UTM_KEYS = ('utm_source', 'utm_medium', 'utm_campaign', 'utm_content')


def campaign_url(url, channel, content=''):
    parts = urlsplit(url)
    values = {key: value for key, value in parse_qsl(parts.query) if not key.startswith('utm_')}
    values.update(utm_source='google', utm_medium='organic', utm_campaign=CAMPAIGNS[channel])
    if content:
        values['utm_content'] = content
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(values), parts.fragment))


class AttributionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.GET.get('utm_source') and not request.session.get('nova_attribution'):
            request.session['nova_attribution'] = {key: request.GET.get(key, '')[:100] for key in UTM_KEYS}
        request.nova_attribution = request.session.get('nova_attribution', {})
        return self.get_response(request)
