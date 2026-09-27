from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from utils import OptimizedImageMixin

class Tour(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(max_length=350)
    body = models.TextField(help_text="Detailed tour description")
    duration_hours = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    capacity = models.PositiveIntegerField(default=8)
    is_private = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=True)
    hotel_pickup_available = models.BooleanField(default=True)
    standard_departure = models.CharField(max_length=200, default="Nova Karagita Base or Approved Partner Jetty")
    best_for = models.CharField(max_length=200, default="Couples, Families, First-time visitors")
    
    route_narrative = models.TextField(blank=True, help_text="Detailed route and scenic narrative")
    what_guests_may_see = models.TextField(
        blank=True,
        help_text="Factual wildlife and scenery expectations without guaranteed sightings"
    )
    inclusions = models.TextField(blank=True, default="Certified captain guide\nLife jackets (adult & child sizes)\nBoat and fuel\nMineral water")
    exclusions = models.TextField(blank=True, default="Crescent Island sanctuary entry fee (payable direct)\nGratuities / tips\nPersonal travel insurance")
    safety_briefing = models.TextField(
        blank=True,
        default="All rides are skippered by licensed local captains. Life jackets are mandatory while on open water. Safe distance is maintained from all wildlife."
    )
    child_policy = models.TextField(
        blank=True,
        default="Children of all ages are welcome with parental supervision. Specialized child-size life jackets are fitted before departure."
    )
    weather_policy = models.TextField(
        blank=True,
        default="Lake Naivasha weather can shift quickly in the late afternoon. If wind or water conditions exceed safety thresholds, departure may be rescheduled or rerouted."
    )
    cancellation_policy = models.TextField(
        blank=True,
        default="Full refund or complimentary reschedule if cancelled due to adverse lake weather conditions."
    )

    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='tours/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='tours/webp/', blank=True, null=True, help_text="480px width optimized")

    @property
    def featured_image(self):
        return self.image or self.webp_image

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    seo_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    verified_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    def get_absolute_url(self):
        return reverse('tours:tour_detail', kwargs={'slug': self.slug})

    @property
    def effective_seo_title(self):
        return self.seo_title or f"{self.name} | Nova Boat Rides Naivasha"

    @property
    def duration_display(self):
        hours = float(self.duration_hours)
        if hours == int(hours):
            hours = int(hours)
        return f"{hours} Hour{'s' if hours != 1 else ''}"

    @property
    def max_capacity(self):
        return self.capacity

    @property
    def crescent_island_included(self):
        return 'crescent' in self.slug

    @property
    def description(self):
        return self.body

    def get_starting_price(self, resident_type='RESIDENT'):
        tier = self.price_tiers.filter(is_active=True, resident_type=resident_type).order_by('amount').first()
        if not tier:
            tier = self.price_tiers.filter(is_active=True).order_by('amount').first()
        return tier.amount if tier else 0

    @property
    def current_rates(self):
        from django.utils import timezone
        today = timezone.now().date()
        rates = self.rates.filter(
            is_active=True,
            is_public=True,
            effective_from__lte=today
        ).filter(
            models.Q(effective_until__isnull=True) | models.Q(effective_until__gte=today)
        ).order_by('amount')
        return rates

    @property
    def canonical_starting_rate_resident(self):
        r = self.current_rates.filter(
            currency='KES',
            audience_type__in=['KENYAN_CITIZEN', 'KENYA_RESIDENT', 'ALL']
        ).first()
        if r:
            return r.amount
        return self.get_starting_price('RESIDENT')

    @property
    def canonical_starting_rate_non_resident(self):
        r = self.current_rates.filter(
            currency='USD',
            audience_type__in=['NON_RESIDENT', 'ALL']
        ).first()
        if r:
            return r.amount
        return self.get_starting_price('NON_RESIDENT')

    @property
    def starting_price_resident(self):
        return self.canonical_starting_rate_resident

    @property
    def starting_price_non_resident(self):
        return self.canonical_starting_rate_non_resident


class ExperienceRate(models.Model):
    """
    Canonical versioned pricing model for Nova boat experiences.
    Central source of truth across homepage, tour detail, /prices/, and quote builders.
    """
    PRICING_MODEL_CHOICES = [
        ('PER_PERSON', 'Per Person'),
        ('PER_BOAT', 'Per Boat'),
        ('PER_GROUP', 'Per Group'),
        ('FROM_PRICE', 'From Price'),
        ('CUSTOM_QUOTE', 'Custom Quote'),
    ]
    AUDIENCE_CHOICES = [
        ('ALL', 'All Visitors'),
        ('KENYAN_CITIZEN', 'Kenyan Citizen'),
        ('KENYA_RESIDENT', 'Kenya Resident'),
        ('NON_RESIDENT', 'Non-Resident / International'),
        ('CHILD', 'Child'),
        ('GROUP', 'Corporate / Group'),
    ]

    experience = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='rates')
    name = models.CharField(max_length=150, help_text="e.g. 1-Hour Private Charter, Shared Seat")
    pricing_model = models.CharField(max_length=30, choices=PRICING_MODEL_CHOICES, default='PER_BOAT')
    currency = models.CharField(max_length=10, default='KES')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    audience_type = models.CharField(max_length=30, choices=AUDIENCE_CHOICES, default='ALL')
    min_guests = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=7)
    duration_minutes = models.PositiveIntegerField(default=60)
    effective_from = models.DateField(default=timezone.now)
    effective_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['experience', 'amount']
        verbose_name = "Experience Rate"
        verbose_name_plural = "Experience Rates"

    def __str__(self):
        return f"{self.experience.name} - {self.name} ({self.currency} {self.amount:,.0f} {self.get_pricing_model_display()})"


class TourPriceTier(models.Model):
    MODE_CHOICES = [
        ('SHARED', 'Shared Boat'),
        ('PRIVATE', 'Private Charter'),
    ]
    RESIDENT_CHOICES = [
        ('RESIDENT', 'Kenyan Resident'),
        ('NON_RESIDENT', 'Non-Resident / International'),
    ]
    PRICING_UNIT_CHOICES = [
        ('PER_PERSON', 'Per Person'),
        ('PER_BOAT', 'Per Boat / Charter'),
    ]

    tour = models.ForeignKey(Tour, related_name='price_tiers', on_delete=models.CASCADE)
    label = models.CharField(max_length=100, help_text="e.g. 1–4 Guests, 5–8 Guests, Full Boat")
    min_guests = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=8)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='SHARED')
    resident_type = models.CharField(max_length=20, choices=RESIDENT_CHOICES, default='RESIDENT')
    pricing_unit = models.CharField(max_length=20, choices=PRICING_UNIT_CHOICES, default='PER_PERSON')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='KES')
    notes = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['tour', 'resident_type', 'amount']
        verbose_name = "Tour Price Tier"
        verbose_name_plural = "Tour Price Tiers"

    def __str__(self):
        return f"{self.tour.name} - {self.label} ({self.currency} {self.amount:.0f})"


class AddOn(models.Model):
    PRICE_MODE_CHOICES = [
        ('FLAT', 'Flat Fee'),
        ('PER_PERSON', 'Per Person'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    price_mode = models.CharField(max_length=20, choices=PRICE_MODE_CHOICES, default='FLAT')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default='KES')
    description = models.TextField(blank=True)
    eligible_tours = models.ManyToManyField(Tour, blank=True, related_name='eligible_addons')
    operational_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Add-On"
        verbose_name_plural = "Add-Ons"

    def __str__(self):
        return f"{self.name} ({self.currency} {self.amount:.0f})"
