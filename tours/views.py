from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from .models import Tour, TourPriceTier, AddOn
from partners.models import HotelPartner

class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'

    def get_queryset(self):
        qs = Tour.objects.filter(is_active=True).order_by('order')
        category = self.request.GET.get('category')
        if category == 'wildlife':
            qs = qs.filter(summary__icontains='hippo') | qs.filter(name__icontains='safari')
        elif category == 'sunset':
            qs = qs.filter(name__icontains='sunset')
        elif category == 'crescent':
            qs = qs.filter(name__icontains='crescent')
        elif category == 'private':
            qs = qs.filter(is_private=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            ('', 'All Rides'),
            ('wildlife', 'Hippo & Wildlife'),
            ('sunset', 'Sunset Cruises'),
            ('crescent', 'Crescent Island'),
            ('private', 'Private Charters'),
        ]
        context['current_category'] = self.request.GET.get('category', '')
        return context


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

    def get_object(self, queryset=None):
        return get_object_or_404(Tour, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.object
        context['price_tiers'] = tour.price_tiers.filter(is_active=True)
        context['add_ons'] = AddOn.objects.filter(is_active=True)
        context['hotel_partners'] = HotelPartner.objects.filter(is_active=True)
        context['related_tours'] = Tour.objects.filter(is_active=True).exclude(pk=tour.pk)[:3]
        return context


class TourQuotePartialView(View):
    """
    HTMX Price Estimator Partial.
    Calculates exact price tier from database based on guest count and residency.
    """
    def get(self, request, slug):
        tour = get_object_or_404(Tour, slug=slug, is_active=True)
        
        try:
            adults = max(1, int(request.GET.get('adults', 2)))
        except ValueError:
            adults = 2
            
        try:
            children = max(0, int(request.GET.get('children', 0)))
        except ValueError:
            children = 0

        total_guests = adults + children
        resident_type = request.GET.get('resident_type', 'RESIDENT')
        is_private = request.GET.get('is_private') == 'true'

        mode = 'PRIVATE' if is_private else 'SHARED'
        
        # Match best price tier
        tiers = tour.price_tiers.filter(
            is_active=True,
            resident_type=resident_type,
            mode=mode,
            min_guests__lte=total_guests,
            max_guests__gte=total_guests
        )
        
        tier = tiers.first()
        if not tier:
            # Fallback to any active tier for this resident type
            tier = tour.price_tiers.filter(is_active=True, resident_type=resident_type).first()

        if tier:
            currency = tier.currency
            if tier.pricing_unit == 'PER_PERSON':
                # Children discount: 50% for children on per-person rides
                boat_total = (tier.amount * adults) + (tier.amount * children * Decimal('0.5'))
            else:
                boat_total = tier.amount
        else:
            currency = "KES"
            boat_total = 3000 * total_guests

        whatsapp_text = (
            f"Hi Nova. I'm checking the {tour.name} for {adults} adult(s)"
            + (f" and {children} child(ren)" if children else "")
            + f". Website estimate: {currency} {boat_total:,.0f}."
        )

        return render(request, 'tours/partials/quote_card.html', {
            'tour': tour,
            'adults': adults,
            'children': children,
            'total_guests': total_guests,
            'resident_type': resident_type,
            'is_private': is_private,
            'tier': tier,
            'currency': currency,
            'boat_total': boat_total,
            'whatsapp_text': whatsapp_text,
        })
