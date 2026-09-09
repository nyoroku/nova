from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import BookingLead
from .forms import BookingLeadForm
from tours.models import Tour
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package
from core.models import SiteSettings

class BookView(View):
    def get(self, request):
        initial = {}
        
        tour_slug = request.GET.get('tour')
        if tour_slug:
            tour = Tour.objects.filter(slug=tour_slug, is_active=True).first()
            if tour:
                initial['tour'] = tour.pk
                initial['lead_type'] = 'BOAT_ONLY'

        hotel_slug = request.GET.get('hotel')
        if hotel_slug:
            hotel = HotelPartner.objects.filter(slug=hotel_slug, is_active=True).first()
            if hotel:
                initial['hotel_partner'] = hotel.pk
                initial['lead_type'] = 'HOTEL_ORIGIN_RIDE'

        pkg_slug = request.GET.get('package')
        if pkg_slug:
            pkg = Package.objects.filter(slug=pkg_slug, is_active=True).first()
            if pkg:
                initial['package'] = pkg.pk
                initial['lead_type'] = 'STAY_AND_RIDE'

        stay_slug = request.GET.get('stay')
        if stay_slug:
            stay = AccommodationProperty.objects.filter(slug=stay_slug, is_active=True).first()
            if stay:
                initial['accommodation_property'] = stay.pk
                initial['lead_type'] = 'ACCOMMODATION'

        form = BookingLeadForm(initial=initial)
        return render(request, 'bookings/book.html', {
            'form': form,
            'settings': SiteSettings.get_solo(),
        })

    def post(self, request):
        form = BookingLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            
            # Extract UTM parameters
            lead.utm_source = request.POST.get('utm_source', '') or request.GET.get('utm_source', '')
            lead.utm_medium = request.POST.get('utm_medium', '') or request.GET.get('utm_medium', '')
            lead.utm_campaign = request.POST.get('utm_campaign', '') or request.GET.get('utm_campaign', '')

            # Calculate server-quoted totals
            boat_amt = 0
            if lead.tour:
                tier = lead.tour.price_tiers.filter(is_active=True).order_by('amount').first()
                if tier:
                    boat_amt = tier.amount * lead.adults + (tier.amount * lead.children * Decimal('0.5'))
            lead.quoted_boat_amount = boat_amt

            positioning_amt = 0
            if lead.hotel_partner and lead.lead_type == 'HOTEL_ORIGIN_RIDE':
                lead.status = 'NEEDS_HOTEL_CONFIRMATION'
                positioning_amt = 2000
            lead.quoted_hotel_logistics_amount = positioning_amt

            stay_amt = 0
            if lead.accommodation_property:
                lead.is_accommodation_provisional = True
                lead.status = 'NEEDS_ACCOMMODATION_CONFIRMATION'
                stay_amt = lead.accommodation_property.starting_price
            lead.quoted_accommodation_amount = stay_amt

            lead.quoted_total_amount = boat_amt + positioning_amt + stay_amt
            lead.save()

            settings_obj = SiteSettings.get_solo()
            whatsapp_url = lead.generate_whatsapp_url(settings_obj.whatsapp_number)

            context = {
                'lead': lead,
                'whatsapp_url': whatsapp_url,
                'settings': settings_obj,
            }

            if request.headers.get('HX-Request'):
                return render(request, 'bookings/partials/booking_success.html', context)
            
            return render(request, 'bookings/booking_success.html', context)

        if request.headers.get('HX-Request'):
            return render(request, 'bookings/partials/form_fields.html', {'form': form})

        return render(request, 'bookings/book.html', {
            'form': form,
            'settings': SiteSettings.get_solo(),
        })
