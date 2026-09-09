from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from utils import OptimizedImageMixin

class HotelPartner(OptimizedImageMixin, models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('RESORT', 'Lakeside Resort'),
        ('LODGE', 'Safari Lodge'),
        ('CAMP', 'Tented Camp'),
        ('BOUTIQUE', 'Boutique Hotel / Villa'),
        ('OTHER', 'Other Lakeside Property'),
    ]
    PARTNERSHIP_STATUS_CHOICES = [
        ('PROSPECT', 'Prospect / Unverified'),
        ('VERIFIED', 'Verified Lake Access / Operational'),
        ('INACTIVE', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='RESORT')
    public_summary = models.TextField(help_text="Public-approved location context and lake proximity")
    website_url = models.URLField(blank=True, help_text="Official hotel website")

    # Strict PRIVATE operations data - NEVER expose to public templates/APIs
    contact_name_private = models.CharField(max_length=150, blank=True, help_text="PRIVATE ops contact name")
    contact_phone_private = models.CharField(max_length=50, blank=True, help_text="PRIVATE ops phone number")
    contact_email_private = models.EmailField(blank=True, help_text="PRIVATE ops email")

    partnership_status = models.CharField(max_length=20, choices=PARTNERSHIP_STATUS_CHOICES, default='PROSPECT')
    marketing_permission = models.BooleanField(
        default=False,
        help_text="Locked rule: Must be True before any co-branding or public partnership claims"
    )
    public_page_enabled = models.BooleanField(
        default=False,
        help_text="Locked rule: Public page is disabled by default. Enabled only with permission and verified service details"
    )
    referral_code = models.CharField(max_length=30, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Commission rate %")

    image = models.ImageField(upload_to='partners/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='partners/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='partners/webp/', blank=True, null=True, help_text="480px width optimized")

    @property
    def featured_image(self):
        return self.image or self.webp_image

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    verified_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Hotel Partner"
        verbose_name_plural = "Hotel Partners"

    def __str__(self):
        return f"{self.name} ({self.get_partnership_status_display()})"

    def clean(self):
        super().clean()
        if self.public_page_enabled and not self.marketing_permission:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'public_page_enabled': "Cannot enable public page without verified marketing permission."
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='image')

    def get_absolute_url(self):
        return reverse('partners:hotel_detail', kwargs={'slug': self.slug})

    @property
    def location_area(self):
        return "South Lake Road, Naivasha"

    @property
    def internal_notes(self):
        return self.public_summary


class HotelServicePoint(models.Model):
    SERVICE_MODE_CHOICES = [
        ('PARTNER_JETTY', 'Direct Hotel Jetty Boarding'),
        ('PARTNER_TRANSFER', 'Road Vehicle Transfer to Nova Base'),
        ('BOAT_POSITIONING', 'Boat Positioned to Approved Access Point'),
        ('REFERRAL_ONLY', 'Standard Launch Departure'),
    ]

    hotel = models.ForeignKey(HotelPartner, related_name='service_points', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, help_text="e.g. Sopa Main Jetty, North Lake Access Point")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    service_mode = models.CharField(max_length=30, choices=SERVICE_MODE_CHOICES, default='PARTNER_TRANSFER')
    
    public_instructions = models.TextField(
        help_text="Guest-facing meeting instructions, security gate guidance, and boarding details"
    )
    private_ops_notes = models.TextField(
        blank=True,
        help_text="PRIVATE captain/ops notes: water depth, mud risks, gate contact, positioning time"
    )
    operating_window = models.CharField(max_length=100, default="07:00 – 17:30")
    notice_hours = models.PositiveIntegerField(
        default=24,
        help_text="Required advance notice in hours for boat positioning or gate clearance"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['hotel', 'name']
        verbose_name = "Hotel Service Point"
        verbose_name_plural = "Hotel Service Points"

    def __str__(self):
        return f"{self.hotel.name} – {self.name} ({self.get_service_mode_display()})"

    @property
    def point_type(self):
        return self.service_mode

    @property
    def get_point_type_display(self):
        return self.get_service_mode_display()

    @property
    def boarding_instructions(self):
        return self.public_instructions

    @property
    def advance_notice_hours(self):
        return self.notice_hours

    @property
    def positioning_fee(self):
        svc = self.tour_services.first()
        return svc.positioning_fee if svc else 0


class HotelTourService(models.Model):
    service_point = models.ForeignKey(HotelServicePoint, related_name='tour_services', on_delete=models.CASCADE)
    tour = models.ForeignKey('tours.Tour', related_name='hotel_services', on_delete=models.CASCADE)
    service_mode = models.CharField(max_length=30, choices=HotelServicePoint.SERVICE_MODE_CHOICES, default='PARTNER_JETTY')
    positioning_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Logistics or positioning fee in KES (0 if complimentary or included in tier)"
    )
    capacity_override = models.PositiveIntegerField(null=True, blank=True)
    allowed_times = models.CharField(max_length=100, default="Morning, Afternoon")
    notice_hours_override = models.PositiveIntegerField(null=True, blank=True)
    requires_manual_confirmation = models.BooleanField(
        default=True,
        help_text="If True, quote flags that boat positioning requires operations sign-off"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['service_point', 'tour']
        unique_together = ('service_point', 'tour')
        verbose_name = "Hotel Tour Service Matrix"
        verbose_name_plural = "Hotel Tour Service Matrix"

    def __str__(self):
        return f"{self.service_point.hotel.name} -> {self.tour.name} (+KES {self.positioning_fee:.0f})"
