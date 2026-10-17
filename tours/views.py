import json
from datetime import date
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from .models import Tour, ServiceIntent, GBPService
from .pricing import quote_activity, valid_on
from core.models import SiteSettings, ExternalFee
from partners.models import HotelAccess


class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        qs = Tour.objects.published().prefetch_related('rates__option', 'images', 'details').order_by('order')
        category = self.request.GET.get('category', '')
        if category in dict(Tour._meta.get_field('category').choices):
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [('','All rides')] + list(Tour._meta.get_field('category').choices)
        context['current_category'] = self.request.GET.get('category', '')
        context['all_tours'] = Tour.objects.published().order_by('order')
        context['hotel_accesses'] = HotelAccess.objects.filter(is_published=True,
            access_status__in=['VERIFIED_ACTIVE', 'VERIFIED_ON_REQUEST']).select_related('property')
        context['services'] = ServiceIntent.objects.filter(is_active=True, level='PRIMARY').select_related('activity')
        context['crescent_fees'] = valid_on(ExternalFee.objects.filter(provider_name__icontains='Crescent'), timezone.localdate())
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

    def get_object(self, queryset=None):
        can_preview = self.request.user.is_staff and self.request.user.has_perm('tours.view_tour')
        qs = Tour.objects.all() if can_preview and self.request.GET.get('preview') == '1' else Tour.objects.published()
        return get_object_or_404(qs, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object
        context['preview'] = self.request.user.is_staff and self.request.user.has_perm('tours.view_tour') and self.request.GET.get('preview') == '1'
        context['gallery'] = list(tour.public_images)
        context['highlights'] = tour.details.filter(kind='HIGHLIGHT')
        context['options'] = tour.options.filter(is_active=True).prefetch_related('rates', 'external_fees')
        context['rates'] = tour.current_rates
        context['related_tours'] = Tour.objects.published().exclude(pk=tour.pk).order_by('order')[:3]
        context['external_fees'] = valid_on(ExternalFee.objects.filter(touroption__tour=tour).distinct(), timezone.localdate())
        context['readiness'] = tour.publication_issues() if context['preview'] else []
        attr = getattr(self.request, 'nova_attribution', None) or {}
        context['attributed_whatsapp_url'] = tour.get_whatsapp_url(
            source_surface=attr.get('source_surface', ''),
            campaign=attr.get('utm_campaign', ''),
            content=attr.get('utm_content', ''),
        )
        config = SiteSettings.get_solo()
        trip_node = {
            '@type': 'TouristTrip',
            'name': tour.name,
            'alternateName': tour.effective_branded_name,
            'description': tour.direct_answer or tour.summary,
            'url': tour.canonical_url,
            'provider': {'@type': 'LocalBusiness', 'name': config.business_name, 'url': settings.SITE_URL},
        }
        if tour.audience_tags:
            trip_node['touristType'] = [t.strip() for t in tour.audience_tags.split(',') if t.strip()]
        elif tour.best_for:
            trip_node['touristType'] = tour.best_for
        start_rate = tour.starting_rate
        if start_rate and start_rate.has_exact_price:
            trip_node['offers'] = {
                '@type': 'Offer',
                'price': str(start_rate.amount),
                'priceCurrency': start_rate.currency,
                'availability': 'https://schema.org/InStock',
                'url': tour.canonical_url,
            }
        graph = [
            trip_node,
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': settings.SITE_URL + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Boat Rides', 'item': settings.SITE_URL + reverse('tours:tour_list')},
                    {'@type': 'ListItem', 'position': 3, 'name': tour.name, 'item': tour.canonical_url},
                ],
            },
        ]
        context['activity_schema'] = json.dumps({'@context':'https://schema.org', '@graph':graph}).replace('<', '\\u003c')
        return context


class TourQuotePartialView(View):
    def get(self, request, slug):
        tour = get_object_or_404(Tour.objects.published(), slug=slug)
        try:
            adults = int(request.GET.get('adults', 1))
            children = int(request.GET.get('children', 0))
            day = date.fromisoformat(request.GET['date']) if request.GET.get('date') else timezone.localdate()
            if day < timezone.localdate():
                raise ValueError('Past date')
            option = request.GET.get('option')
            if option and not option.isdigit():
                raise ValueError('Invalid option')
        except (ValueError, TypeError):
            return render(request, 'tours/partials/quote_card.html', {'tour':tour, 'input_error':'Choose a valid date and party size.'}, status=400)
        quote = quote_activity(tour, adults=adults, children=children, service_date=day,
            currency=request.GET.get('currency', 'KES'), visitor_type=request.GET.get('visitor_type', request.GET.get('resident_type', 'RESIDENT')),
            option_id=option, private=request.GET.get('is_private') == 'true')
        from urllib.parse import urlencode
        enquiry = tour.enquiry_url + '&' + urlencode({'option':quote.option.pk if quote.option else '',
            'preferred_date':str(day), 'adults':adults, 'children':children, 'currency':quote.currency,
            'visitor_type':request.GET.get('visitor_type', 'RESIDENT')})
        response = render(request, 'tours/partials/quote_card.html', {'tour':tour, 'quote':quote, 'enquiry_context_url':enquiry})
        response['X-Robots-Tag'] = 'noindex, nofollow'
        response['Cache-Control'] = 'no-store'
        return response


class ServicesView(ListView):
    template_name = 'tours/services.html'
    context_object_name = 'services'
    def get_queryset(self):
        return ServiceIntent.objects.filter(is_active=True).select_related('activity')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = dict(Tour._meta.get_field('category').choices)
        labels['hotel'] = 'Hotel departures'
        groups = {}
        for service in context['services']:
            destination = service.destination
            if not destination:
                continue
            group = groups.setdefault(service.category, {'name': labels.get(service.category, service.category), 'items': [], 'destinations': set()})
            if destination not in group['destinations']:
                group['items'].append(service)
                group['destinations'].add(destination)
        context['service_groups'] = list(groups.values())
        context['gbp_services'] = GBPService.objects.filter(is_active=True).select_related('activity').order_by('number', 'name')
        return context
