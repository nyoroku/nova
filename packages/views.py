from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from .models import Package
from tours.models import Tour
from stays.models import AccommodationProperty

class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        return Package.objects.filter(is_active=True).prefetch_related('components').order_by('order')


class PackageDetailView(DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_object(self, queryset=None):
        return get_object_or_404(Package, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pkg = self.object
        context['components'] = pkg.components.order_by('order')
        context['tours'] = pkg.eligible_tours.filter(is_active=True)
        context['stays'] = pkg.accommodation_properties.filter(is_active=True)
        return context


class PackageQuotePartialView(View):
    """
    HTMX Package Quote Builder Partial.
    Adheres to Master Spec §7.3 & §15:
    Componentizes known boat price, hotel logistics, and marks accommodation as
    provisional/awaiting confirmation if needed.
    """
    def get(self, request, slug):
        package = get_object_or_404(Package, slug=slug, is_active=True)

        try:
            adults = max(1, int(request.GET.get('adults', 2)))
        except ValueError:
            adults = 2
            
        try:
            children = max(0, int(request.GET.get('children', 0)))
        except ValueError:
            children = 0

        stay_id = request.GET.get('stay_id')
        selected_stay = None
        if stay_id and stay_id.isdigit():
            selected_stay = AccommodationProperty.objects.filter(pk=int(stay_id), is_active=True).first()

        # Estimated boat portion
        tour = package.eligible_tours.filter(is_active=True).first()
        boat_amount = 0
        if tour:
            boat_amount = tour.get_starting_price() * adults + (tour.get_starting_price() * children * Decimal('0.5'))

        # Hotel logistics portion
        positioning_amount = 2000 if package.includes_hotel_origin_pickup else 0

        # Accommodation portion
        stay_amount = 0
        is_provisional = True
        if selected_stay:
            if selected_stay.inventory_mode in ['MANAGED', 'ALLOTMENT'] and selected_stay.starting_price > 0:
                stay_amount = selected_stay.starting_price * package.duration_nights
                is_provisional = False
            else:
                stay_amount = selected_stay.starting_price * package.duration_nights
                is_provisional = True

        total_estimate = boat_amount + positioning_amount + stay_amount

        whatsapp_text = (
            f"Hi Nova. I would like to book the {package.name} for {adults} adult(s)"
            + (f" and {children} child(ren)" if children else "")
            + (f" at {selected_stay.name}" if selected_stay else "")
            + f". Total estimate: KES {total_estimate:,.0f}"
            + (" (accommodation subject to confirmation)" if is_provisional else "")
            + "."
        )

        return render(request, 'packages/partials/package_quote_card.html', {
            'package': package,
            'adults': adults,
            'children': children,
            'selected_stay': selected_stay,
            'boat_amount': boat_amount,
            'positioning_amount': positioning_amount,
            'stay_amount': stay_amount,
            'total_estimate': total_estimate,
            'is_provisional': is_provisional,
            'whatsapp_text': whatsapp_text,
        })
