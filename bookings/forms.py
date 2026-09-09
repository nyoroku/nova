from django import forms
from .models import BookingLead
from tours.models import Tour
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package

class BookingLeadForm(forms.ModelForm):
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
        self.fields['tour'].queryset = Tour.objects.filter(is_active=True)
        self.fields['hotel_partner'].queryset = HotelPartner.objects.filter(is_active=True)
        self.fields['accommodation_property'].queryset = AccommodationProperty.objects.filter(is_active=True)
        self.fields['package'].queryset = Package.objects.filter(is_active=True)
        
        # Apply clean Nova Electric styling classes
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'nova-checkbox'
            else:
                field.widget.attrs['class'] = 'nova-form-input'
