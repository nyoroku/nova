from django.db import models

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
    email = models.EmailField(default="hello@novaboatrider.com")
    
    standard_launch_name = models.CharField(max_length=150, default="Nova Karagita Base, Lake Naivasha")
    standard_launch_lat = models.DecimalField(max_digits=9, decimal_places=6, default=-0.762030)
    standard_launch_lng = models.DecimalField(max_digits=9, decimal_places=6, default=36.425790)
    operating_hours = models.CharField(max_length=100, default="Daily 6:30 AM – 6:30 PM")
    default_currency = models.CharField(max_length=5, default="KES")
    gbp_url = models.URLField(blank=True, default="")
    directions_summary = models.TextField(
        blank=True,
        default="Located at Karagita Beach off Moi South Lake Road, Naivasha (8 km from Naivasha Town). Dedicated briefing pavilion, secure perimeter parking, life jacket fitting station, and direct boat jetty access."
    )
    booking_notice = models.CharField(
        max_length=255,
        default="Advance notice recommended for hotel pickups, Crescent Island walks, and sunset charters."
    )
    last_verified_at = models.DateField(auto_now=True)

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
