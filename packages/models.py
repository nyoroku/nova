from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from utils import OptimizedImageMixin

class Package(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    tagline = models.CharField(max_length=200, default="Stay + Ride + Explore")
    summary = models.CharField(max_length=350)
    description = models.TextField()

    hero_image = models.ImageField(upload_to='packages/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='packages/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='packages/webp/', blank=True, null=True, help_text="480px width optimized")

    @property
    def featured_image(self):
        return self.hero_image or self.webp_image

    eligible_tours = models.ManyToManyField('tours.Tour', blank=True, related_name='packages')
    accommodation_properties = models.ManyToManyField('stays.AccommodationProperty', blank=True, related_name='packages')

    duration_days = models.PositiveIntegerField(default=2)
    duration_nights = models.PositiveIntegerField(default=1)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=5, default="KES")
    price_basis = models.CharField(max_length=100, default="per couple / 1 night + boat ride")

    includes_hotel_origin_pickup = models.BooleanField(default=True)
    includes_crescent_island = models.BooleanField(default=False)
    includes_transfers = models.BooleanField(default=False)
    itinerary_summary = models.TextField(blank=True, help_text="Chronological itinerary narrative")

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    verified_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.hero_image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='hero_image')

    def get_absolute_url(self):
        return reverse('packages:package_detail', kwargs={'slug': self.slug})


class PackageComponent(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('BOAT', 'Lake Boat Safari'),
        ('HOTEL', 'Lakeside Accommodation'),
        ('TRANSFER', 'Private Road Transfer'),
        ('ACTIVITY', 'Crescent Island / Hell\'s Gate Adventure'),
        ('MEAL', 'Lakeside Dining / Picnic'),
    ]

    package = models.ForeignKey(Package, related_name='components', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES, default='BOAT')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['package', 'order']
        verbose_name = "Package Component"
        verbose_name_plural = "Package Components"

    def __str__(self):
        return f"{self.package.name} – {self.title} ({self.get_component_type_display()})"

    @property
    def is_included(self):
        return True
