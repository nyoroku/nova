from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import HotelPartner, HotelServicePoint, HotelTourService

class HotelTourServiceInline(admin.TabularInline):
    model = HotelTourService
    extra = 1

class HotelServicePointInline(admin.StackedInline):
    model = HotelServicePoint
    extra = 1

@admin.register(HotelPartner)
class HotelPartnerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'property_type', 'partnership_status',
        'marketing_permission', 'public_page_enabled', 'is_active', 'verified_at'
    )
    list_filter = ('partnership_status', 'marketing_permission', 'public_page_enabled', 'is_active')
    search_fields = ('name', 'public_summary', 'contact_name_private')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HotelServicePointInline]

    fieldsets = (
        ("Public Presentation", {
            "fields": ("name", "slug", "property_type", "public_summary", "website_url", "image", "order", "is_active")
        }),
        ("Marketing & Page Publication Gate", {
            "fields": ("partnership_status", "marketing_permission", "public_page_enabled"),
            "description": "Public page can only be enabled if marketing permission is verified and public summary is provided."
        }),
        ("PRIVATE Operational Contacts (Never Public)", {
            "fields": ("contact_name_private", "contact_phone_private", "contact_email_private"),
            "classes": ("collapse",),
            "description": "Internal operations reference only. This information is excluded from all public templates and APIs."
        }),
        ("B2B / Settlement", {
            "fields": ("referral_code", "commission_rate"),
            "classes": ("collapse",)
        }),
    )

    def clean(self):
        super().clean()
        if self.public_page_enabled and not self.marketing_permission:
            raise ValidationError("Cannot enable a public hotel page without explicit marketing permission.")


@admin.register(HotelServicePoint)
class HotelServicePointAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'service_mode', 'operating_window', 'notice_hours', 'is_active')
    list_filter = ('service_mode', 'is_active')
    search_fields = ('hotel__name', 'name')
    inlines = [HotelTourServiceInline]


@admin.register(HotelTourService)
class HotelTourServiceAdmin(admin.ModelAdmin):
    list_display = ('service_point', 'tour', 'service_mode', 'positioning_fee', 'requires_manual_confirmation', 'is_active')
    list_filter = ('service_mode', 'requires_manual_confirmation', 'is_active')
