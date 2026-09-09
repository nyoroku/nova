from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import AccommodationProperty
from tours.models import Tour

class StayListView(ListView):
    model = AccommodationProperty
    template_name = 'stays/stay_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        qs = AccommodationProperty.objects.filter(is_active=True).order_by('order')
        inv_mode = self.request.GET.get('mode')
        if inv_mode:
            qs = qs.filter(inventory_mode=inv_mode)
        prop_type = self.request.GET.get('type')
        if prop_type:
            qs = qs.filter(property_type=prop_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modes'] = AccommodationProperty.INVENTORY_MODE_CHOICES
        context['property_types'] = AccommodationProperty.PROPERTY_TYPE_CHOICES
        context['current_mode'] = self.request.GET.get('mode', '')
        context['current_type'] = self.request.GET.get('type', '')
        return context


class StayDetailView(DetailView):
    model = AccommodationProperty
    template_name = 'stays/stay_detail.html'
    context_object_name = 'property'

    def get_object(self, queryset=None):
        return get_object_or_404(AccommodationProperty, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = self.object.room_types.filter(is_active=True)
        context['pairable_tours'] = Tour.objects.filter(is_active=True)[:3]
        return context
