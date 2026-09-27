from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from utils import OptimizedImageMixin

class Captain(OptimizedImageMixin, models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    role_title = models.CharField(max_length=120, default="Senior Lake Captain")
    photo = models.ImageField(upload_to='crew/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='crew/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='crew/webp/', blank=True, null=True, help_text="480px width optimized")

    @property
    def featured_image(self):
        return self.photo or self.webp_image

    bio = models.TextField()
    years_on_lake = models.PositiveIntegerField(default=10)
    route_specialties = models.CharField(
        max_length=255,
        default="Hippo family territories, fish eagle calling, Crescent Island western approach"
    )
    languages = models.CharField(max_length=120, default="English, Swahili")
    quote = models.CharField(
        max_length=255,
        default="The lake has its own rhythm. When you start early and respect the wind, every ride is smooth."
    )
    certification_text = models.CharField(
        max_length=255,
        default="KMA Licensed Coxswain & Lake Safety Certified",
        blank=True
    )
    certification_issuer = models.CharField(
        max_length=120,
        default="Kenya Maritime Authority",
        blank=True
    )
    certification_reference = models.CharField(max_length=100, blank=True)
    verified_at = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Captain"
        verbose_name_plural = "Captains"

    def __str__(self):
        return f"{self.name} ({self.role_title})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.photo and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='photo')


class GuideArticle(OptimizedImageMixin, models.Model):
    CATEGORY_CHOICES = [
        ('PLANNING', 'Trip Planning'),
        ('WILDLIFE', 'Wildlife & Birds'),
        ('HOTEL_LOGISTICS', 'Hotel & Jetty Logistics'),
        ('SAFETY', 'Water Safety & Weather'),
        ('CAPTAIN_LOG', 'Captain\'s Field Log'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.CharField(max_length=300)
    body = models.TextField()
    author = models.CharField(max_length=100, default="Nova Lake Operations")
    reviewer = models.CharField(max_length=100, default="Senior Captain Team")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='PLANNING')
    direct_quick_answer = models.TextField(
        blank=True,
        help_text="AEO concise direct answer block for AI search extraction"
    )
    hero_image = models.ImageField(upload_to='journal/', blank=True, null=True)
    webp_image = models.ImageField(upload_to='journal/webp/', blank=True, null=True)
    webp_mobile = models.ImageField(upload_to='journal/webp/', blank=True, null=True)

    @property
    def featured_image(self):
        return self.hero_image or self.webp_image

    published_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    verified_at = models.DateField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    seo_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ['-is_featured', '-published_at']
        verbose_name = "Guide Article"
        verbose_name_plural = "Guide Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.hero_image and (not self.webp_image or not self.webp_mobile):
            self.convert_to_webp(source_field_name='hero_image')

    def get_absolute_url(self):
        return reverse('content:journal_detail', kwargs={'slug': self.slug})

    @property
    def summary(self):
        return self.excerpt

    @property
    def content(self):
        return self.body

    @property
    def author_captain(self):
        return Captain.objects.filter(is_active=True).first()

    @property
    def reading_time_minutes(self):
        words = len(self.body.split())
        return max(3, round(words / 220))


class QuestionAnswer(models.Model):
    CATEGORY_CHOICES = [
        ('HOTEL_PICKUP', 'Hotel Pickup & Departures'),
        ('PRICES', 'Pricing & Payments'),
        ('CHILDREN', 'Children & Families'),
        ('WEATHER', 'Weather & Lake Conditions'),
        ('CRESCENT', 'Crescent Island'),
        ('SAFETY', 'Safety & Gear'),
        ('BOOKING', 'Booking & Lead Time'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    plain_answer = models.TextField(blank=True, help_text="Plain text concise answer for AI / Rich Snippet extractability")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='HOTEL_PICKUP')
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "Question & Answer"
        verbose_name_plural = "Questions & Answers"

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    SEGMENT_CHOICES = [
        ('HOTEL_GUEST', 'Hotel Guest'),
        ('COUPLE', 'Couple / Celebration'),
        ('FAMILY', 'Family with Children'),
        ('GROUP', 'Group / Corporate Retreat'),
        ('PHOTOGRAPHER', 'Photographer / Creator'),
    ]

    guest_name = models.CharField(max_length=120)
    guest_segment = models.CharField(max_length=30, choices=SEGMENT_CHOICES, default='HOTEL_GUEST')
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    source = models.CharField(max_length=50, default="Verified Post-Trip Guest")
    trip_date = models.CharField(max_length=50, default="September 2026")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.guest_name} ({self.get_guest_segment_display()}) - {self.rating} stars"


class ReviewSnapshot(models.Model):
    """
    Dated snapshot of external review platforms (Google Business Profile, TripAdvisor, etc.).
    Avoids self-serving LocalBusiness aggregateRating schema while providing
    honest, verified third-party review stats to visitors.
    """
    SOURCE_CHOICES = [
        ('GOOGLE_MAPS', 'Google Business Profile'),
        ('TRIPADVISOR', 'TripAdvisor'),
        ('DIRECT', 'Direct Guest Survey'),
    ]

    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='GOOGLE_MAPS')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.90)
    review_count = models.PositiveIntegerField(default=48)
    source_url = models.URLField(
        default="https://maps.google.com/?cid=12648759322304975239",
        blank=True
    )
    captured_at = models.DateField(default=timezone.now)
    is_current = models.BooleanField(default=True)
    summary_quote = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-captured_at']
        verbose_name = "Review Snapshot"
        verbose_name_plural = "Review Snapshots"

    def __str__(self):
        return f"{self.get_source_display()}: {self.rating} stars ({self.review_count} reviews) as of {self.captured_at.strftime('%B %Y')}"


class ArticleSource(models.Model):
    """
    Citations and verifiable evidence for facts stated in guide articles
    (tariffs, government gazettes, GPS observations, hotel communications).
    """
    SOURCE_TYPE_CHOICES = [
        ('OFFICIAL_TARIFF', 'Official Tariff Notice'),
        ('GOVERNMENT', 'Government Agency (KWS / KMA)'),
        ('FIELD_OBSERVATION', 'Captain Log / Field Observation'),
        ('HOTEL_CONFIRMATION', 'Hotel Management Written Confirmation'),
        ('RESEARCH_PAPER', 'Research Publication'),
    ]

    article = models.ForeignKey(GuideArticle, on_delete=models.CASCADE, related_name='sources')
    source_name = models.CharField(max_length=200, help_text="e.g. Crescent Island Game Sanctuary Tariff Schedule 2026")
    source_url = models.URLField(blank=True)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPE_CHOICES, default='OFFICIAL_TARIFF')
    claim_supported = models.CharField(max_length=255, blank=True, help_text="e.g. Adult resident entrance fee is KES 1,100")
    verified_at = models.DateField(default=timezone.now)
    display_publicly = models.BooleanField(default=True)

    class Meta:
        ordering = ['article', 'id']
        verbose_name = "Article Source Citation"
        verbose_name_plural = "Article Source Citations"

    def __str__(self):
        return f"{self.article.title[:30]}... -> {self.source_name}"

