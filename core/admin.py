from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand Identity (Locked Nova Electric)", {
            "fields": ("business_name", "legal_name", "tagline", "supporting_proposition", "default_currency")
        }),
        ("Contact & WhatsApp Direct", {
            "fields": ("phone_display", "phone_e164", "whatsapp_number", "email", "gbp_url")
        }),
        ("Operations & Standard Launch", {
            "fields": ("standard_launch_name", "standard_launch_lat", "standard_launch_lng", "operating_hours", "directions_summary", "booking_notice")
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
