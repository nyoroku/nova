from django.contrib import admin
from .models import SiteSettings, ExternalFee, BusinessFact, ClaimEvidence

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ("gbp_website_url", "same_as_urls")
    fieldsets = (
        ("Brand Identity (Locked Nova Electric)", {
            "fields": ("business_name", "legal_name", "tagline", "supporting_proposition", "default_currency")
        }),
        ("Contact & WhatsApp Direct", {
            "fields": ("phone_display", "phone_e164", "whatsapp_number", "email", "gbp_url", "google_business_profile_url", "gbp_website_url", "google_maps_url", "facebook_url", "instagram_url", "tiktok_url", "same_as_urls", "response_expectation")
        }),
        ("Physical Address & Local SEO", {
            "fields": ("street_address", "locality", "county", "country")
        }),
        ("Operations & Hours", {
            "fields": ("standard_launch_name", "standard_launch_lat", "standard_launch_lng", "operating_hours", "opening_time", "closing_time", "directions_summary", "booking_notice")
        }),
        ("Analytics & Verification", {
            "fields": ("ga4_measurement_id", "ga4_setup_verified")
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
    search_fields = ('provider_name', 'service_name', 'notes', 'disclaimer')


@admin.register(BusinessFact)
class BusinessFactAdmin(admin.ModelAdmin):
    list_display = ('key', 'public_label', 'value', 'last_verified_at', 'verification_source', 'active', 'is_stale')
    list_filter = ('active', 'verification_source')
    search_fields = ('key', 'public_label', 'value')


@admin.register(ClaimEvidence)
class ClaimEvidenceAdmin(admin.ModelAdmin):
    list_display = ('claim_key', 'evidence_type', 'verified_at', 'expires_at', 'publishable', 'is_stale')
    list_filter = ('evidence_type', 'publishable')
    search_fields = ('claim_key', 'claim_text', 'evidence_reference')


