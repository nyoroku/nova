from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from django.http import Http404
from .models import HotelPartner, HotelServicePoint, HotelTourService
from tours.models import Tour

class HotelHubView(ListView):
    model = HotelPartner
    template_name = 'partners/hotel_hub.html'
    context_object_name = 'partners'

    def get_queryset(self):
        return HotelPartner.objects.filter(is_active=True).prefetch_related('service_points')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tours'] = Tour.objects.filter(is_active=True)
        return context


class HotelDetailView(DetailView):
    model = HotelPartner
    template_name = 'partners/hotel_detail.html'
    context_object_name = 'partner'

    def get_object(self, queryset=None):
        partner = get_object_or_404(HotelPartner, slug=self.kwargs['slug'], is_active=True)
        # Strict gate: Only publish if marketing permission is verified and public page is enabled!
        if not (partner.marketing_permission and partner.public_page_enabled):
            raise Http404("This hotel does not have an active public page.")
        return partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_points'] = self.object.service_points.filter(is_active=True)
        context['tours'] = Tour.objects.filter(is_active=True)
        return context


class HotelCheckerPartialView(View):
    """
    HTMX Hotel Serviceability Checker Partial.
    Evaluates whether Nova can board at a hotel jetty, arrange road pickup,
    or position a boat with fee and notice disclosure.
    """
    def get(self, request):
        hotel_id = request.GET.get('hotel_id')
        custom_name = request.GET.get('custom_hotel_name', '').strip()
        tour_slug = request.GET.get('tour_slug', '')

        selected_hotel = None
        service_point = None
        tour_service = None

        if hotel_id and hotel_id.isdigit():
            selected_hotel = HotelPartner.objects.filter(pk=int(hotel_id), is_active=True).first()
            if selected_hotel:
                service_point = selected_hotel.service_points.filter(is_active=True).first()
                if service_point and tour_slug:
                    tour_service = service_point.tour_services.filter(
                        tour__slug=tour_slug,
                        is_active=True
                    ).first()

        return render(request, 'partners/partials/serviceability_result.html', {
            'hotel': selected_hotel,
            'custom_name': custom_name,
            'service_point': service_point,
            'tour_service': tour_service,
        })
