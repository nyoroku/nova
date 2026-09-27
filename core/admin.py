from django.contrib import admin
from .models import SiteSettings, ExternalFee

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand Identity (Locked Nova Electric)", {
            "fields": ("business_name", "legal_name", "tagline", "supporting_proposition", "default_currency")
        }),
        ("Contact & WhatsApp Direct", {
            "fields": ("phone_display", "phone_e164", "whatsapp_number", "email", "gbp_url", "google_maps_url")
        }),
        ("Physical Address & Local SEO", {
            "fields": ("street_address", "locality", "county", "postal_code", "country")
        }),
        ("Operations & Hours", {
            "fields": ("standard_launch_name", "standard_launch_lat", "standard_launch_lng", "operating_hours", "opening_time", "closing_time", "directions_summary", "booking_notice")
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ExternalFee)
class ExternalFeeAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'service_name', 'visitor_type', 'adult_amount', 'child_amount', 'currency', 'last_verified_at', 'is_active')
    list_filter = ('provider_name', 'visitor_type', 'currency', 'is_active')
    search_fields = ('provider_name', 'service_name', 'notes')

