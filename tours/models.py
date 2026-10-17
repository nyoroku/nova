from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.functional import cached_property
from utils import OptimizedImageMixin

class TourQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_active=True, status='PUBLISHED')

class Tour(OptimizedImageMixin, models.Model):
    objects = TourQuerySet.as_manager()
    STATUS_CHOICES = [(s, s.replace('_', ' ').title()) for s in
                      ('DRAFT', 'FACT_CHECK', 'READY', 'PUBLISHED', 'PAUSED', 'ARCHIVED')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    legacy_publication = models.BooleanField(default=False, editable=False)
    internal_name = models.CharField(max_length=200, blank=True)
    branded_name = models.CharField(max_length=200, blank=True, help_text="Optional Nova secondary label, e.g. Nova Classic Lake Safari")
    gbp_activity_name = models.CharField(max_length=200, blank=True, help_text="Approved Google Business Profile Activity name")
    primary_intent = models.CharField(max_length=120, blank=True, help_text="Primary query cluster / search intent")
    audience_tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated audience tags")
    review_prompt = models.CharField(max_length=300, blank=True, help_text="Experience-specific honest feedback prompt for guests (§10.1)")
    legacy_body = models.TextField(blank=True, editable=False)
    duration_minutes = models.PositiveIntegerField(default=60)
    category = models.CharField(max_length=30, default='wildlife', choices=[
        ('wildlife', 'Wildlife'), ('crescent', 'Crescent Island'), ('private', 'Private'),
        ('family', 'Family'), ('sunrise-sunset', 'Sunrise & Sunset'),
        ('birding', 'Birding & Photography'), ('groups', 'Groups')])
    booking_mode = models.CharField(max_length=20, default='ENQUIRY', choices=[('ENQUIRY', 'Availability enquiry')])
    direct_answer = models.TextField(blank=True)
    meeting_point = models.TextField(blank=True)
    arrival_minutes_before = models.PositiveIntegerField(default=15)
    what_to_bring = models.TextField(blank=True)
    accessibility_notes = models.TextField(blank=True)
    operational_verified_at = models.DateField(null=True, blank=True)
    verification_evidence = models.TextField(blank=True, help_text='Internal evidence supporting operational facts')
    operations_owner = models.CharField(max_length=150, blank=True)
    google_activity_enabled = models.BooleanField(default=False)
    connectivity_provider = models.CharField(max_length=100, blank=True)
    external_product_id = models.CharField(max_length=100, blank=True)
    external_booking_url = models.URLField(blank=True)
    google_submission_status = models.CharField(max_length=20, default='NOT_SUBMITTED', choices=[
        ('NOT_SUBMITTED', 'Not submitted'), ('SUBMITTED', 'Submitted'),
        ('ACCEPTED', 'Accepted by channel'), ('REJECTED', 'Rejected by channel')])
    updated_at = models.DateTimeField(auto_now=True)
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
        if self.pk:
            gallery_image = self.public_images.first()
            if gallery_image:
                return gallery_image.webp_image or gallery_image.image
            if self.images.exists():
                return None
        for image in (self.webp_image, self.image):
            if image and image.storage.exists(image.name):
                return image
        return None

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
        return f"{self.duration_minutes} minutes"

    @property
    def public_duration_display(self):
        durations = sorted(set(self.options.filter(is_active=True).values_list('duration_minutes', flat=True)))
        if len(durations) > 1:
            return f'{durations[0]}–{durations[-1]} minutes (choose an option)'
        return f'{durations[0]} minutes' if durations else self.duration_display

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
        currency = 'USD' if resident_type == 'NON_RESIDENT' else 'KES'
        rate = next((r for r in self.catalogue_rates if r.currency == currency), None)
        return rate.amount if rate else None

    @property
    def current_rates(self):
        from django.utils import timezone
        today = timezone.localdate()
        rates = self.rates.filter(
            is_active=True,
            is_public=True,
            effective_from__lte=today
        ).filter(
            models.Q(effective_until__isnull=True) | models.Q(effective_until__gte=today)
        ).filter(option__is_active=True, option__tour_id=self.pk, amount__gte=0,
                 duration_minutes=models.F('option__duration_minutes'), min_guests=models.F('option__min_guests'),
                 max_guests=models.F('option__max_guests')).select_related('option').order_by('option__order', 'amount')
        return rates

    @cached_property
    def catalogue_rates(self):
        return sorted(self.current_rates.exclude(pricing_model__in=['CUSTOM_QUOTE', 'FROM_PRICE']).exclude(audience_type='CHILD'),
                      key=lambda r: (r.currency, r.minimum_total, r.option.order, r.pk))

    @cached_property
    def starting_rate(self):
        return next((r for r in self.catalogue_rates if r.currency == 'KES'), None)

    @cached_property
    def matching_usd_rate(self):
        start = self.starting_rate
        return next((r for r in self.catalogue_rates if start and r.currency == 'USD'
                     and r.option_id == start.option_id and r.pricing_model == start.pricing_model), None)

    @cached_property
    def public_images(self):
        return self.images.filter(is_published=True).order_by('-is_primary', 'display_order', 'pk')[:15]

    @property
    def inclusion_items(self):
        return list(self.details.filter(kind='INCLUDED').values_list('text', flat=True)) or self.inclusions.splitlines()

    @property
    def exclusion_items(self):
        return list(self.details.filter(kind='EXCLUDED').values_list('text', flat=True)) or self.exclusions.splitlines()

    @property
    def canonical_url(self):
        return settings.SITE_URL.rstrip('/') + self.get_absolute_url()

    @property
    def effective_branded_name(self):
        if self.branded_name:
            return self.branded_name
        if self.internal_name:
            return self.internal_name if self.internal_name.startswith('Nova') else f"Nova {self.internal_name}"
        return ''

    @property
    def effective_gbp_activity_name(self):
        return self.gbp_activity_name or self.name

    @property
    def short_answer(self):
        return self.direct_answer or self.summary

    @property
    def gbp_activity_enabled(self):
        return self.google_activity_enabled

    @property
    def last_verified_at(self):
        return self.operational_verified_at

    @property
    def gbp_booking_url(self):
        from .attribution import campaign_url
        return campaign_url(self.canonical_url, 'activity', self.slug)

    @property
    def enquiry_url(self):
        return reverse('bookings:book') + '?tour=' + self.slug

    def get_whatsapp_url(self, source_surface='', campaign='', content=''):
        from urllib.parse import urlencode
        from core.models import SiteSettings
        attr_note = ''
        if campaign or source_surface:
            ref_parts = [p for p in (source_surface, campaign, content or self.slug) if p]
            attr_note = f"\nSource ref: {' / '.join(ref_parts)}"
        message = (f"Hi Nova Boat Rides Naivasha, I'd like to enquire about {self.name} ({self.slug}). "
                   'Preferred date: \nPreferred time: \nAdults: \nChildren: \nHotel / starting location: \n'
                   f'Please confirm availability and total price.{attr_note}')
        return 'https://wa.me/' + SiteSettings.get_solo().whatsapp_number + '?' + urlencode({'text': message})

    @property
    def whatsapp_url(self):
        return self.get_whatsapp_url()

    def publication_issues(self, google=False):
        from .readiness import publication_issues
        return publication_issues(self, google=google)

    def clean(self):
        super().clean()
        continuing_legacy = self.pk and self.legacy_publication and self.status == 'PUBLISHED' and type(self).objects.filter(
            pk=self.pk, status='PUBLISHED', legacy_publication=True).exists()
        if self.status in ('READY', 'PUBLISHED') and not continuing_legacy:
            issues = self.publication_issues() if self.pk else ['Save as draft and complete the publication checklist.']
            if issues:
                raise ValidationError({'status': issues})

    @property
    def canonical_starting_rate_resident(self):
        return self.starting_rate.amount if self.starting_rate else None

    @property
    def canonical_starting_rate_non_resident(self):
        return self.matching_usd_rate.amount if self.matching_usd_rate else None

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
    option = models.ForeignKey('TourOption', null=True, blank=True, on_delete=models.PROTECT, related_name='rates')
    child_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                     help_text='Explicit child seat rate; blank means request a quote for children')
    verified_at = models.DateField(null=True, blank=True)
    verification_evidence = models.TextField(blank=True)
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

    @property
    def minimum_total(self):
        return self.amount * self.min_guests if self.pricing_model == 'PER_PERSON' else self.amount

    @property
    def unit_label(self):
        return {'PER_PERSON': 'per person', 'PER_BOAT': 'per boat', 'PER_GROUP': 'per group',
                'CUSTOM_QUOTE': 'custom quote', 'FROM_PRICE': 'from price — request a quote'}.get(self.pricing_model, '')

    @property
    def has_exact_price(self):
        return self.pricing_model in ('PER_PERSON', 'PER_BOAT', 'PER_GROUP')

    def clean(self):
        super().clean()
        errors = {}
        if self.amount < 0 or (self.child_amount is not None and self.child_amount < 0):
            errors['amount'] = 'Amounts cannot be negative.'
        if self.effective_until and self.effective_until < self.effective_from:
            errors['effective_until'] = 'End date must follow the start date.'
        if self.min_guests < 1 or self.max_guests < self.min_guests:
            errors['max_guests'] = 'Guest bounds are invalid.'
        if self.option and (self.option.tour_id != self.experience_id or self.duration_minutes != self.option.duration_minutes
                            or self.min_guests != self.option.min_guests or self.max_guests != self.option.max_guests):
            errors['option'] = 'Rate tour, duration and guest bounds must match its booking option.'
        if self.is_active and self.experience_id:
            qs = ExperienceRate.objects.filter(
                experience_id=self.experience_id,
                option_id=self.option_id,
                currency=self.currency,
                audience_type=self.audience_type,
                pricing_model=self.pricing_model,
                duration_minutes=self.duration_minutes,
                is_active=True,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if self.effective_until:
                qs = qs.filter(effective_from__lte=self.effective_until)
            if self.effective_from:
                qs = qs.filter(models.Q(effective_until__isnull=True) | models.Q(effective_until__gte=self.effective_from))
            if qs.exists():
                errors['effective_from'] = 'Conflicting active rate overlaps for the same experience, option, currency, audience and pricing model.'
        if errors:
            raise ValidationError(errors)


class TourOption(models.Model):
    tour = models.ForeignKey(Tour, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=180)
    mode = models.CharField(max_length=20, choices=[('SHARED', 'Shared seats'), ('PRIVATE', 'Private boat'), ('GROUP', 'Group booking')])
    duration_minutes = models.PositiveIntegerField()
    min_guests = models.PositiveIntegerField(default=1)
    max_guests = models.PositiveIntegerField(default=7)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    verified_at = models.DateField(null=True, blank=True)
    verification_evidence = models.TextField(blank=True)
    external_fees = models.ManyToManyField('core.ExternalFee', blank=True,
        help_text='Mandatory fees paid at the activity; choose every applicable audience category')

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.tour.name}: {self.name} ({self.duration_minutes} min, {self.get_mode_display()})'

    def clean(self):
        if self.min_guests < 1 or self.max_guests < self.min_guests or self.duration_minutes < 1:
            raise ValidationError('Duration and guest bounds must be valid.')


class ActivityDetail(models.Model):
    tour = models.ForeignKey(Tour, related_name='details', on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=[('HIGHLIGHT', 'Highlight'), ('INCLUDED', 'Included'), ('EXCLUDED', 'Excluded')])
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']


class ItineraryStep(models.Model):
    tour = models.ForeignKey(Tour, related_name='itinerary_steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']


class ActivityFAQ(models.Model):
    tour = models.ForeignKey(Tour, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=240)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']


class ActivityImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activities/originals/%Y/%m/')
    webp_image = models.ImageField(upload_to='activities/optimized/', blank=True)
    webp_mobile = models.ImageField(upload_to='activities/optimized/', blank=True)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    content_hash = models.CharField(max_length=64, blank=True, editable=False)
    role = models.CharField(max_length=20, default='GALLERY', choices=[(x, x.title()) for x in
        ['HERO', 'GALLERY', 'WILDLIFE', 'PEOPLE', 'CAPTAIN', 'BOARDING', 'SCENERY', 'ROUTE', 'DETAIL']])
    alt_text = models.CharField(max_length=220)
    caption = models.CharField(max_length=300, blank=True)
    credit = models.CharField(max_length=180, blank=True)
    rights_confirmed = models.BooleanField(default=False, help_text='Nova has permission, including consent for identifiable guests')
    is_primary = models.BooleanField(default=False)
    google_activity_eligible = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'pk']
        constraints = [models.UniqueConstraint(fields=['tour'], condition=models.Q(is_primary=True), name='one_primary_activity_image')]

    def clean(self):
        super().clean()
        if self.google_activity_eligible and not self.rights_confirmed:
            raise ValidationError({'google_activity_eligible': 'Confirm image rights before Google use.'})
        previous = type(self).objects.filter(pk=self.pk).first() if self.pk else None
        new_publication = not previous or not previous.is_published or previous.image.name != self.image.name
        if self.is_published and new_publication and not self.rights_confirmed:
            raise ValidationError({'rights_confirmed': 'Confirm image rights and guest consent, or save this image unpublished.'})

    @property
    def google_url(self):
        url = (self.webp_image or self.image).url
        return url if url.startswith(('https://', 'http://')) else settings.SITE_URL.rstrip('/') + url

    def save(self, *args, **kwargs):
        import hashlib
        from io import BytesIO
        from PIL import Image, ImageOps
        from django.core.files.base import ContentFile
        changed = kwargs.pop('optimize', False) or not self.pk or (self.image and not self.image._committed)
        if changed and self.image:
            self.image.open('rb')
            original = self.image.read()
            self.image.seek(0)
            digest = hashlib.sha256(original).hexdigest()
            if (digest == self.content_hash and self.width and self.webp_image and self.webp_mobile
                    and self.webp_image.storage.exists(self.webp_image.name) and self.webp_mobile.storage.exists(self.webp_mobile.name)):
                return super().save(*args, **kwargs)
            self.content_hash = digest
            with Image.open(BytesIO(original)) as source:
                picture = ImageOps.exif_transpose(source).convert('RGB')
                self.width, self.height = picture.size
                for field, size in [('webp_image', 1280), ('webp_mobile', 480)]:
                    derivative = picture.copy()
                    derivative.thumbnail((size, size))
                    buffer = BytesIO()
                    derivative.save(buffer, 'WEBP', quality=82)
                    getattr(self, field).save(self.content_hash[:20] + f'-{size}.webp', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)


class ServiceIntent(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=[('PRIMARY', 'Primary'), ('SECONDARY', 'Secondary')])
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=300, blank=True)
    activity = models.ForeignKey(Tour, null=True, blank=True, related_name='service_intents', on_delete=models.SET_NULL)
    destination_name = models.CharField(max_length=60, blank=True, help_text='Named Django route for hubs')
    is_active = models.BooleanField(default=True)
    operational_verified_at = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order', 'pk']

    @property
    def destination(self):
        if self.activity_id:
            return self.activity.get_absolute_url() if self.activity.is_active and self.activity.status == 'PUBLISHED' else ''
        return reverse(self.destination_name) if self.destination_name else ''

    def clean(self):
        if bool(self.activity_id) == bool(self.destination_name):
            raise ValidationError('Choose exactly one activity or named hub destination.')
        if self.destination_name:
            from django.urls import NoReverseMatch
            try:
                url = reverse(self.destination_name)
                if url.startswith('/admin/'):
                    raise ValidationError('Choose a public hub route.')
            except NoReverseMatch:
                raise ValidationError({'destination_name': 'Unknown route name.'})


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


class GBPService(models.Model):
    """
    Canonical 16 Google Business Profile Services (§5.5) with approved copy,
    query cluster, wave priority, and website landing-page mapping.
    """
    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    primary_cluster = models.CharField(max_length=120)
    wave = models.PositiveSmallIntegerField(default=1)
    activity = models.ForeignKey(Tour, null=True, blank=True, related_name='gbp_services', on_delete=models.SET_NULL)
    destination_name = models.CharField(max_length=60, blank=True, help_text='Named Django route if mapping to a hub')
    show_price_in_gbp = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    excluded_reason = models.CharField(max_length=255, blank=True)
    last_verified_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['number']
        verbose_name = "GBP Canonical Service"
        verbose_name_plural = "GBP Canonical Services"

    def __str__(self):
        return f"#{self.number} {self.name}"

    @property
    def destination_url(self):
        if self.activity_id:
            if self.activity.is_active and self.activity.status == 'PUBLISHED':
                return self.activity.get_absolute_url()
            return '/boat-rides/'
        if self.destination_name:
            return reverse(self.destination_name)
        return '/boat-rides/'

    @property
    def destination(self):
        return self.destination_url

    @property
    def service_name(self):
        return self.name

    @property
    def gbp_category_name(self):
        return self.primary_cluster

    @property
    def short_description(self):
        return self.description

    @property
    def order(self):
        return self.number

    @property
    def canonical_rate_display(self):
        if self.show_price_in_gbp and self.activity_id and self.activity.starting_rate:
            r = self.activity.starting_rate
            return f"{r.currency} {r.amount:,.0f} {r.unit_label}"
        return ''

    def clean(self):
        import re
        if re.search(r'(?:KES|USD|Ksh|\$|\+254|07\d{8}|\d{7,})', self.name, re.I):
            raise ValidationError({'name': 'GBP service names must not contain phone numbers or prices (§5.6).'})


class GBPQueryScorecard(models.Model):
    """
    Monthly Google Business Profile query-breadth and AI visibility scorecard (§12.5).
    Editable in Django Admin without code changes (§17.31).
    """
    period_label = models.CharField(max_length=60, unique=True, help_text="e.g. Baseline (Oct 2026), Month 1, Month 2, Month 3")
    period_start = models.DateField(default=timezone.now)
    unique_discovery_queries = models.PositiveIntegerField(default=0)
    lake_naivasha_boat_ride_searches = models.PositiveIntegerField(default=0)
    boat_ride_on_lake_naivasha_searches = models.PositiveIntegerField(default=0)
    lake_naivasha_tour_searches = models.PositiveIntegerField(default=0)
    tourist_attraction_naivasha_searches = models.PositiveIntegerField(default=0)
    crescent_island_searches = models.PositiveIntegerField(default=0)
    boat_safari_hippo_searches = models.PositiveIntegerField(default=0)
    price_cost_searches = models.PositiveIntegerField(default=0)
    family_couple_group_searches = models.PositiveIntegerField(default=0)
    website_clicks = models.PositiveIntegerField(default=0)
    calls = models.PositiveIntegerField(default=0)
    directions = models.PositiveIntegerField(default=0)
    tracked_whatsapp_clicks = models.PositiveIntegerField(default=0)
    gsc_ai_impressions = models.PositiveIntegerField(default=0, help_text="Google Search Console Generative AI impressions")
    bing_ai_citations = models.PositiveIntegerField(default=0, help_text="Bing Webmaster Tools AI Performance total citations")
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['period_start', 'pk']
        verbose_name = "GBP & AI Monthly Scorecard"
        verbose_name_plural = "GBP & AI Monthly Scorecards"

    def __str__(self):
        return f"{self.period_label} ({self.unique_discovery_queries} discovery queries)"


class GBPPostTheme(models.Model):
    """
    Rotating 4-week GBP post cadence (§10.3) with UTM link generation.
    """
    week_number = models.PositiveSmallIntegerField(default=1)
    post_order = models.PositiveSmallIntegerField(default=1)
    theme_title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180, unique=True)
    target_cluster = models.CharField(max_length=120)
    suggested_summary = models.TextField()
    activity = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.SET_NULL, related_name='gbp_post_themes')
    destination_name = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['week_number', 'post_order']
        verbose_name = "GBP Post Cadence Theme"
        verbose_name_plural = "GBP Post Cadence Themes"

    def __str__(self):
        return f"Week {self.week_number}.{self.post_order}: {self.theme_title}"

    @property
    def destination_url(self):
        base = settings.SITE_URL.rstrip('/')
        if self.activity_id and self.activity.is_active and self.activity.status == 'PUBLISHED':
            path = self.activity.get_absolute_url()
        elif self.destination_name:
            path = reverse(self.destination_name)
        else:
            path = '/boat-rides/'
        from .attribution import campaign_url
        return campaign_url(base + path, 'post', self.slug)

    @property
    def title(self):
        return self.theme_title

    @property
    def gbp_cta_url(self):
        return self.destination_url


