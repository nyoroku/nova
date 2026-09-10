import uuid
import urllib.parse
from django.db import models
from django.utils import timezone

def generate_booking_reference():
    date_str = timezone.now().strftime("%Y%m%d")
    unique_suffix = uuid.uuid4().hex[:4].upper()
    return f"NOV-{date_str}-{unique_suffix}"

class BookingLead(models.Model):
    LEAD_TYPE_CHOICES = [
        ('BOAT_ONLY', 'Standard Boat Experience'),
        ('HOTEL_ORIGIN_RIDE', 'Hotel-Origin Boat Departure'),
        ('ACCOMMODATION', 'Accommodation Enquiry'),
        ('STAY_AND_RIDE', 'Stay + Ride Package'),
        ('FULL_DAY_PACKAGE', 'Full Day Lake Itinerary'),
        ('GROUP_CORPORATE', 'Corporate / Group Event'),
        ('SPECIAL_EVENT', 'Special Celebration / Sunset Charter'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'New Enquiry'),
        ('NEEDS_HOTEL_CONFIRMATION', 'Awaiting Hotel Clearance / Positioning Confirmation'),
        ('NEEDS_ACCOMMODATION_CONFIRMATION', 'Awaiting Room Rate / Availability Confirmation'),
        ('QUOTED', 'Quote Sent to Guest'),
        ('DEPOSIT_PENDING', 'Deposit Pending'),
        ('CONFIRMED', 'Booking Confirmed'),
        ('COMPLETED', 'Trip Completed'),
        ('CANCELLED', 'Cancelled'),
        ('LOST', 'Lost / Expired'),
    ]

    TRANSPORT_CHOICES = [
        ('NONE', 'No Road Transport (Self-Drive / Own Arrangements)'),
        ('NAIROBI_TRANSFER', 'Private Nairobi <-> Naivasha Vehicle Transfer'),
        ('NAIVASHA_LOCAL', 'Naivasha Local Hotel / SGR Station Transfer'),
    ]

    reference = models.CharField(max_length=30, unique=True, default=generate_booking_reference)
    lead_type = models.CharField(max_length=35, choices=LEAD_TYPE_CHOICES, default='BOAT_ONLY')
    status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='NEW')

    # Guest Details
    guest_name = models.CharField(max_length=150)
    guest_phone = models.CharField(max_length=50)
    guest_email = models.EmailField(blank=True)
    
    # Schedule & Party
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, default="Morning (08:30)")
    adults = models.PositiveIntegerField(default=2)
    children = models.PositiveIntegerField(default=0)
    is_private_requested = models.BooleanField(default=False)

    # Experience Linkages
    tour = models.ForeignKey('tours.Tour', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    hotel_partner = models.ForeignKey('partners.HotelPartner', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    service_point = models.ForeignKey('partners.HotelServicePoint', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    custom_hotel_name = models.CharField(max_length=200, blank=True, help_text="Hotel name if not in partner list")

    accommodation_property = models.ForeignKey('stays.AccommodationProperty', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')
    room_preference = models.CharField(max_length=150, blank=True)
    package = models.ForeignKey('packages.Package', null=True, blank=True, on_delete=models.SET_NULL, related_name='leads')

    transport_required = models.CharField(max_length=30, choices=TRANSPORT_CHOICES, default='NONE')
    special_requests = models.TextField(blank=True)

    # Transparent Pricing Breakdown
    quoted_boat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quoted_hotel_logistics_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quoted_accommodation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quoted_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=5, default="KES")
    is_accommodation_provisional = models.BooleanField(default=False)

    # Attribution & Operations
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    consent_operational = models.BooleanField(default=True)
    internal_notes = models.TextField(blank=True, help_text="Internal operations notes (never visible to guest)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking Lead"
        verbose_name_plural = "Booking Leads"

    def __str__(self):
        return f"{self.reference} - {self.guest_name} ({self.get_lead_type_display()}) [{self.get_status_display()}]"

    def generate_whatsapp_message(self):
        """
        Adheres to Master Spec §16.4:
        'Hi Nova. I’m planning [experience] on [date] for [party size].
         I am [staying at HOTEL / not staying at a hotel].
         I’m interested in [hotel pickup / accommodation / stay + ride].
         Website estimate: [KES X or “pending accommodation confirmation”].'
        """
        experience_name = "a lake experience"
        if self.tour:
            experience_name = self.tour.name
        elif self.package:
            experience_name = self.package.name

        party_size = f"{self.adults} adult{'s' if self.adults != 1 else ''}"
        if self.children > 0:
            party_size += f", {self.children} child{'ren' if self.children != 1 else ''}"

        hotel_status = "not staying at a hotel"
        if self.hotel_partner:
            hotel_status = f"staying at {self.hotel_partner.name}"
        elif self.custom_hotel_name:
            hotel_status = f"staying at {self.custom_hotel_name}"

        interest = "boat ride"
        if self.lead_type == 'HOTEL_ORIGIN_RIDE':
            interest = "hotel pickup / jetty departure"
        elif self.lead_type == 'STAY_AND_RIDE':
            interest = "stay + ride package"
        elif self.lead_type == 'ACCOMMODATION':
            interest = "accommodation booking"

        if self.is_accommodation_provisional or (self.accommodation_property and self.quoted_accommodation_amount == 0):
            estimate_str = "pending accommodation confirmation"
        elif self.quoted_total_amount > 0:
            estimate_str = f"{self.currency} {self.quoted_total_amount:,.0f}"
        else:
            estimate_str = "standard rate upon review"

        return (
            f"Hi Nova. I’m planning {experience_name} on {self.preferred_date} for {party_size}. "
            f"I am {hotel_status}. I’m interested in {interest}. "
            f"Website estimate: {estimate_str}. (Ref: {self.reference})"
        )

    def generate_whatsapp_url(self, whatsapp_number="254701215295"):
        msg = self.generate_whatsapp_message()
        encoded = urllib.parse.quote(msg)
        return f"https://wa.me/{whatsapp_number}?text={encoded}"

    @property
    def reference_number(self):
        return self.reference
