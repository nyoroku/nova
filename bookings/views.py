import uuid
from django.db import transaction
from django.shortcuts import render
from django.views.generic import View
from .models import BookingLead
from .forms import BookingLeadForm
from tours.models import Tour
from tours.pricing import quote_activity
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package
from core.models import SiteSettings
from tours.attribution import UTM_KEYS


def booking_options(request):
    tour_id = request.GET.get('tour', '')
    tour = Tour.objects.published().filter(pk=tour_id).first() if tour_id.isdigit() else None
    options = tour.options.filter(is_active=True) if tour else []
    response = render(request, 'bookings/partials/option_choices.html', {'options':options})
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response


class BookView(View):
    def get(self, request):
        initial = {}
        for key, model, field, lead_type in [
            ('tour', Tour, 'tour', 'BOAT_ONLY'), ('hotel', HotelPartner, 'hotel_partner', 'HOTEL_ORIGIN_RIDE'),
            ('package', Package, 'package', 'STAY_AND_RIDE'), ('stay', AccommodationProperty, 'accommodation_property', 'ACCOMMODATION')]:
            query = model.objects.published() if model is Tour else model.objects.filter(is_active=True)
            obj = query.filter(slug=request.GET.get(key)).first()
            if obj:
                initial.update({field: obj.pk, 'lead_type': lead_type})
        tour = Tour.objects.published().filter(pk=initial.get('tour')).first()
        option = tour.options.filter(pk=request.GET.get('option'), is_active=True).first() if tour and request.GET.get('option', '').isdigit() else None
        if option:
            initial['option'] = option.pk
        for key in ('adults', 'children'):
            if request.GET.get(key, '').isdigit() and 0 <= int(request.GET[key]) <= 500:
                initial[key] = int(request.GET[key])
        for key, allowed in [('currency', ('KES', 'USD')), ('visitor_type', ('CITIZEN', 'RESIDENT', 'NON_RESIDENT'))]:
            if request.GET.get(key) in allowed:
                initial[key] = request.GET[key]
        if request.GET.get('preferred_date'):
            from datetime import date
            try:
                day = date.fromisoformat(request.GET['preferred_date'])
                initial['preferred_date'] = day
            except ValueError:
                pass
        token = str(uuid.uuid4())
        request.session['nova_submission_tokens'] = (request.session.get('nova_submission_tokens', []) + [token])[-20:]
        initial['submission_token'] = token
        return render(request, 'bookings/book.html', {'form': BookingLeadForm(initial=initial), 'selected_tour': tour})

    def post(self, request):
        form = BookingLeadForm(request.POST)
        token = request.POST.get('submission_token', '')
        if token not in request.session.get('nova_submission_tokens', []):
            form.is_valid()
            form.add_error(None, 'Please reopen the enquiry form before submitting.')
        elif form.is_valid():
            with transaction.atomic():
                existing = BookingLead.objects.filter(submission_key=form.cleaned_data['submission_token']).first()
                if existing:
                    return self.success(request, existing)
                lead = form.save(commit=False)
                lead.submission_key = form.cleaned_data['submission_token']
                attribution = getattr(request, 'nova_attribution', {})
                for key in UTM_KEYS:
                    setattr(lead, key, attribution.get(key, '')[:100])
                if lead.tour:
                    quote = quote_activity(lead.tour, adults=lead.adults, children=lead.children,
                        visitor_type=lead.visitor_type, currency=lead.currency, service_date=lead.preferred_date,
                        option_id=lead.option_id, private=lead.is_private_requested,
                        hotel=lead.hotel_partner if lead.lead_type == 'HOTEL_ORIGIN_RIDE' else None)
                    extra = []
                    if lead.transport_required not in ('', 'NONE'):
                        extra.append('Road transport needs a separate confirmed quote.')
                    if lead.lead_type == 'HOTEL_ORIGIN_RIDE':
                        lead.status = 'NEEDS_HOTEL_CONFIRMATION'
                        if not lead.hotel_partner:
                            extra.append('Hotel departure and logistics charges require confirmation.')
                    if lead.accommodation_property or lead.package:
                        extra.append('Accommodation and package pricing require staff confirmation.')
                    quote.reasons.extend(extra)
                    if extra:
                        quote.total = None
                    lead.quote_complete = quote.complete
                    lead.option = quote.option
                    lead.quote_snapshot = quote.snapshot()
                    lead.quote_snapshot.update(activity_name=lead.tour.name,
                        service_date=str(lead.preferred_date), cancellation_policy=lead.tour.cancellation_policy,
                        weather_policy=lead.tour.weather_policy)
                    lead.quoted_boat_amount = quote.boat_amount or 0
                    lead.quoted_hotel_logistics_amount = quote.hotel_amount
                    lead.quoted_total_amount = quote.total if quote.complete else 0
                else:
                    lead.quote_snapshot = {'reasons': ['Our team will confirm your complete package price.'], 'total': None}
                if lead.accommodation_property:
                    lead.is_accommodation_provisional = True
                    lead.status = 'NEEDS_ACCOMMODATION_CONFIRMATION'
                defaults = {field.attname: getattr(lead, field.attname) for field in BookingLead._meta.concrete_fields
                            if field.name not in ('id', 'submission_key', 'created_at', 'updated_at')}
                lead, created = BookingLead.objects.get_or_create(submission_key=lead.submission_key, defaults=defaults)
            return self.success(request, lead, submitted=created)
        template = 'bookings/partials/booking_form.html' if request.headers.get('HX-Request') else 'bookings/book.html'
        return render(request, template, {'form': form}, status=200)

    def success(self, request, lead, submitted=False):
        settings_obj = SiteSettings.get_solo()
        context = {'lead': lead, 'settings': settings_obj, 'submitted': submitted,
                   'whatsapp_url': lead.generate_whatsapp_url(settings_obj.whatsapp_number)}
        template = 'bookings/partials/booking_success.html' if request.headers.get('HX-Request') else 'bookings/booking_success.html'
        response = render(request, template, context)
        response['Cache-Control'] = 'no-store'
        if submitted:
            import json
            response['HX-Trigger'] = json.dumps({'booking_enquiry_submit': {'activity_slug': lead.tour.slug if lead.tour else ''}})
        return response
