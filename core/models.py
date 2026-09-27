from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    """
    Singleton model managing Nova site-wide identity, contact,
    location, and operational parameters.
    """
    business_name = models.CharField(max_length=150, default="Nova Boat Rides Naivasha")
    legal_name = models.CharField(max_length=150, default="Nova Boat Rides Naivasha Ltd")
    tagline = models.CharField(max_length=200, default="Naivasha starts here.")
    supporting_proposition = models.CharField(
        max_length=300,
        default="Boat rides, hotel departures and curated stays around Lake Naivasha — planned through one local team."
    )
    phone_display = models.CharField(max_length=50, default="+254 701 215 295")
    phone_e164 = models.CharField(max_length=30, default="+254701215295")
    whatsapp_number = models.CharField(max_length=30, default="254701215295")
    email = models.EmailField(default="hello@novaboatridesnaivasha.co.ke")

    # Physical Address & Location
    street_address = models.CharField(max_length=200, default="Karagita Beach, Moi South Lake Road")
    locality = models.CharField(max_length=100, default="Karagita, Naivasha")
    county = models.CharField(max_length=100, default="Nakuru County")
    country = models.CharField(max_length=100, default="Kenya")
    standard_launch_name = models.CharField(max_length=150, default="Nova Karagita Base, Lake Naivasha")
    standard_launch_lat = models.DecimalField(max_digits=9, decimal_places=6, default=-0.762030)
    standard_launch_lng = models.DecimalField(max_digits=9, decimal_places=6, default=36.425790)

    # Operational Hours
    opening_time = models.CharField(max_length=10, default="06:30")
    closing_time = models.CharField(max_length=10, default="18:30")
    operating_hours = models.CharField(max_length=100, default="Daily 6:30 AM – 6:30 PM")
    default_currency = models.CharField(max_length=5, default="KES")

    # Links & Integrations
    google_maps_url = models.URLField(blank=True, default="https://maps.google.com/?q=-0.762030,36.425790")
    google_business_profile_url = models.URLField(blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    tiktok_url = models.URLField(blank=True, default="")
    tripadvisor_url = models.URLField(blank=True, default="")
    gbp_url = models.URLField(blank=True, default="")

    directions_summary = models.TextField(
        blank=True,
        default="Located at Karagita Beach off Moi South Lake Road, Naivasha (8 km from Naivasha Town). Dedicated briefing pavilion, secure perimeter parking, life jacket fitting station, and direct boat jetty access."
    )
    booking_notice = models.CharField(
        max_length=255,
        default="Advance notice recommended for hotel pickups, Crescent Island walks, and sunset charters."
    )
    default_meta_image = models.ImageField(upload_to="meta/", blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    last_verified_at = models.DateField(auto_now=True)

    @property
    def legal_business_name(self):
        return self.legal_name

    @property
    def primary_phone(self):
        return self.phone_display

    @property
    def latitude(self):
        return self.standard_launch_lat

    @property
    def longitude(self):
        return self.standard_launch_lng

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ExternalFee(models.Model):
    """
    Tracks third-party admission and attraction fees separately from Nova boat rates.
    Sources official schedules with date verification.
    """
    VISITOR_TYPES = [
        ('CITIZEN', 'Kenyan Citizen'),
        ('RESIDENT', 'East African Resident'),
        ('NON_RESIDENT', 'Non-Resident (International)'),
        ('STUDENT', 'Student'),
        ('ALL', 'All Visitors'),
    ]

    provider_name = models.CharField(max_length=150, help_text="e.g. Crescent Island Game Sanctuary, Kenya Wildlife Service")
    service_name = models.CharField(max_length=150, help_text="e.g. Sanctuary Entry, Park Entry")
    visitor_type = models.CharField(max_length=30, choices=VISITOR_TYPES, default='ALL')
    adult_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    child_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    student_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='KES')
    effective_from = models.DateField(null=True, blank=True)
    effective_until = models.DateField(null=True, blank=True)
    source_url = models.URLField(blank=True, default="https://www.crescentisland.co/")
    source_name = models.CharField(max_length=150, blank=True, default="Official Conservation Schedule")
    last_verified_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "External Fee"
        verbose_name_plural = "External Fees"
        ordering = ['provider_name', 'visitor_type']

    def __str__(self):
        return f"{self.provider_name} - {self.service_name} ({self.get_visitor_type_display()}): {self.currency} {self.adult_amount}"

