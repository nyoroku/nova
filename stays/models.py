import builtins
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from utils import OptimizedImageMixin

class AccommodationProperty(OptimizedImageMixin, models.Model):
    INVENTORY_MODE_CHOICES = [
        ('ENQUIRY', 'Enquiry / Request Availability'),
        ('ALLOTMENT', 'Provisional Allocation (Staff Confirmation)'),
        ('MANAGED', 'Managed Inventory (Confirmed by Nova)'),
        ('EXTERNAL_BOOK', 'External Booking / Referral'),
    ]
    PROPERTY_TYPE_CHOICES = [
        ('RESORT', 'Lakeside Resort'),
        ('LODGE', 'Safari Lodge'),
        ('CAMP', 'Tented Camp'),
        ('BOUTIQUE', 'Boutique Hotel / Villa'),
        ('COTTAGES', 'Lakeside Cottages'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    partner = models.ForeignKey(
        'partners.HotelPartner',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='accommodations',
        help_text="Link to partner record if hotel-origin boat departures are supported"
    )
    inventory_mode = models.CharField(
        max_length=20,
        choices=INVENTORY_MODE_CHOICES,
        default='ENQUIRY',
        help_text="Locked rule: Must accurately declare whether availability is live, provisional, or enquiry-only"
    )
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='RESORT')
    address = models.CharField(max_length=255, default="Lake Naivasha, Kenya")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    summary = models.CharField(max_length=350)
    description = models.TextField()
    why_nova_recommends = models.TextField(
        help_text="Why this property works with a Nova lake day: water access, jetty proximity, family suitability"
    )
    amenities = models.TextField(
        default="Lakefront Gardens, Swimming Pool, Restaurant & Bar, Wi-Fi, Secure Parking",
        help_text="Comma-separated or bullet list of verified property amenities"
    )
    check_in_time = models.CharField(max_length=50, default="14:00")
    check_out_time = models.CharField(max_length=50, default="10:00")
    child_policy = models.TextField(blank=True, default="Children welcome. Extra beds and family rooms available upon request.")
    cancellation_policy = models.TextField(blank=True, default="Cancellation policies depend on property terms and season.")
    official_url = models.URLField(blank=True, help_text="Official website of the property")

    image = models.ImageField(upload_to='stays/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='stays/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='stays/webp/', blank=True, null=True, help_text="480px width optimized")

    @property
    def featured_image(self):
        return self.image or self.webp_image

    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=5, default="KES")
    price_basis = models.CharField(max_length=100, default="per room / night (BB)")

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    verified_at = models.DateField(auto_now=True)

    seo_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Accommodation Property"
        verbose_name_plural = "Accommodation Properties"

    def __str__(self):
        return f"{self.name} ({self.get_inventory_mode_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    def get_absolute_url(self):
        return reverse('stays:stay_detail', kwargs={'slug': self.slug})

    @property
    def location_area(self):
        return self.address

    @property
    def has_jetty_access(self):
        if self.partner:
            return self.partner.service_points.filter(service_mode='PARTNER_JETTY').exists()
        return False


class RoomType(models.Model):
    property = models.ForeignKey(AccommodationProperty, related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, help_text="e.g. Standard Lakeview Room, Cottage, Deluxe Suite")
    max_adults = models.PositiveIntegerField(default=2)
    max_children = models.PositiveIntegerField(default=1)
    bed_configuration = models.CharField(max_length=150, default="1 King Bed or 2 Twin Beds")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stays/rooms/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['property', 'name']
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"

    def __str__(self):
        return f"{self.property.name} - {self.name}"

    @builtins.property
    def max_occupancy(self):
        return self.max_adults + self.max_children


class AccommodationRate(models.Model):
    MEAL_PLAN_CHOICES = [
        ('RO', 'Room Only'),
        ('BB', 'Bed & Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive'),
    ]
    PRICING_MODE_CHOICES = [
        ('PER_ROOM', 'Per Room / Night'),
        ('PER_PERSON', 'Per Person / Night'),
    ]
    RESIDENT_CHOICES = [
        ('RESIDENT', 'Kenyan Resident'),
        ('NON_RESIDENT', 'Non-Resident / International'),
    ]

    room_type = models.ForeignKey(RoomType, related_name='rates', on_delete=models.CASCADE)
    meal_plan = models.CharField(max_length=10, choices=MEAL_PLAN_CHOICES, default='BB')
    pricing_mode = models.CharField(max_length=20, choices=PRICING_MODE_CHOICES, default='PER_ROOM')
    resident_type = models.CharField(max_length=20, choices=RESIDENT_CHOICES, default='RESIDENT')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default="KES")
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    inventory_quantity = models.PositiveIntegerField(default=5)
    is_available = models.BooleanField(default=True)
    verified_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['room_type', 'meal_plan', 'amount']
        verbose_name = "Accommodation Rate"
        verbose_name_plural = "Accommodation Rates"

    def __str__(self):
        return f"{self.room_type} ({self.get_meal_plan_display()}) - {self.currency} {self.amount:.0f}"
