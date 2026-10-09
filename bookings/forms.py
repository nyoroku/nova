from django import forms
from .models import BookingLead
from tours.models import Tour, TourOption
from django.utils import timezone
from django.urls import reverse
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package

class BookingLeadForm(forms.ModelForm):
    submission_token = forms.UUIDField(widget=forms.HiddenInput)
    consent_operational = forms.BooleanField(required=True, label='I agree to operational booking messages.')
    class Meta:
        model = BookingLead
        fields = [
            'lead_type',
            'guest_name',
            'guest_phone',
            'guest_email',
            'preferred_date',
            'preferred_time',
            'adults',
            'children',
            'is_private_requested',
            'tour',
            'option',
            'visitor_type',
            'currency',
            'hotel_partner',
            'custom_hotel_name',
            'accommodation_property',
            'room_preference',
            'package',
            'transport_required',
            'special_requests',
            'consent_operational',
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Wildlife interests, dietary preferences, celebratory setups, luggage...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transport_required'].required = False
        self.fields['transport_required'].initial = 'NONE'
        self.fields['tour'].queryset = Tour.objects.published()
        self.fields['option'].queryset = TourOption.objects.filter(tour__status='PUBLISHED', tour__is_active=True, is_active=True)
        self.fields['option'].required = False
        self.fields['option'].empty_label = 'Please recommend an option'
        self.fields['option'].label = 'Booking option'
        self.fields['tour'].label = 'Activity'
        self.fields['lead_type'].label = 'Departure or package request'
        self.fields['transport_required'].label = 'Road transport preference'
        self.fields['children'].label = 'Children (add their ages in your notes)'
        self.fields['is_private_requested'].label = 'Require a private boat'
        selected_tour = self.data.get('tour') if self.is_bound else self.initial.get('tour')
        if selected_tour and str(selected_tour).isdigit():
            self.fields['option'].queryset = self.fields['option'].queryset.filter(tour_id=selected_tour)
            self.fields['option'].label_from_instance = lambda option: f'{option.name} · {option.min_guests}–{option.max_guests} guests'
        self.fields['tour'].widget.attrs.update({'hx-get':reverse('bookings:options'), 'hx-trigger':'change',
            'hx-target':'#id_option', 'hx-swap':'innerHTML', 'hx-include':'#id_tour'})
        self.fields['currency'] = forms.ChoiceField(choices=[('KES', 'Kenyan shillings (KES)'), ('USD', 'US dollars (USD)')], initial='KES')
        self.fields['adults'].min_value = 1
        self.fields['adults'].max_value = 500
        self.fields['children'].max_value = 500
        self.fields['preferred_date'].widget.attrs['min'] = timezone.localdate().isoformat()
        self.fields['consent_operational'].initial = False
        self.fields['hotel_partner'].queryset = HotelPartner.objects.filter(is_active=True)
        self.fields['accommodation_property'].queryset = AccommodationProperty.objects.filter(is_active=True)
        self.fields['package'].queryset = Package.objects.filter(is_active=True)
        
        # Apply clean Nova Electric styling classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'nova-checkbox'
            else:
                field.widget.attrs['class'] = 'nova-form-input'

    def clean(self):
        cleaned = super().clean()
        tour, option = cleaned.get('tour'), cleaned.get('option')
        if option and (not tour or option.tour_id != tour.pk):
            self.add_error('option', 'Choose an option for the selected activity.')
        if cleaned.get('lead_type') in ('BOAT_ONLY', 'HOTEL_ORIGIN_RIDE') and not tour:
            self.add_error('tour', 'Choose your activity.')
        if option and cleaned.get('is_private_requested') and option.mode == 'SHARED':
            self.add_error('option', 'Select a private option or ask us to recommend one.')
        if cleaned.get('preferred_date') and cleaned['preferred_date'] < timezone.localdate():
            self.add_error('preferred_date', 'Choose today or a future date.')
        return cleaned

    @property
    def field_groups(self):
        return [
            ('Your activity and party', [self[x] for x in ['tour', 'option', 'preferred_date', 'preferred_time', 'adults', 'children', 'visitor_type', 'currency']]),
            ('Your contact details', [self[x] for x in ['guest_name', 'guest_phone', 'guest_email']]),
            ('Departure and other requests', [self[x] for x in ['lead_type', 'is_private_requested', 'hotel_partner', 'custom_hotel_name',
                'accommodation_property', 'room_preference', 'package', 'transport_required', 'special_requests']]),
        ]
