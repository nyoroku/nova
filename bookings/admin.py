from django.contrib import admin
from django.utils.html import format_html
from .models import BookingLead

@admin.register(BookingLead)
class BookingLeadAdmin(admin.ModelAdmin):
    change_list_template = 'bookings/admin_lead_list.html'
    list_display = (
        'reference', 'guest_name', 'guest_phone', 'lead_type',
        'preferred_date', 'status', 'quoted_total_amount', 'currency', 'whatsapp_link', 'created_at'
    )
    list_filter = ('status', 'lead_type', 'is_private_requested', 'transport_required', 'created_at')
    search_fields = ('reference', 'guest_name', 'guest_phone', 'guest_email', 'custom_hotel_name')
    readonly_fields = ('reference', 'created_at', 'updated_at', 'whatsapp_preview', 'quote_snapshot')

    fieldsets = (
        ("Reference & Lead State", {
            "fields": ("reference", "status", "lead_type", "created_at", "assigned_to", "contacted_at", "confirmed_at", "completed_at", "actual_revenue")
        }),
        ("Guest Information", {
            "fields": ("guest_name", "guest_phone", "guest_email", "consent_operational")
        }),
        ("Trip Parameters", {
            "fields": ("preferred_date", "preferred_time", "adults", "children", "is_private_requested", "transport_required", "special_requests")
        }),
        ("Linked Products", {
            "fields": ("tour", "option", "visitor_type", "hotel_partner", "service_point", "custom_hotel_name", "accommodation_property", "room_preference", "package")
        }),
        ("Quoted Financials", {
            "fields": ("quote_complete", "quote_snapshot", "quoted_boat_amount", "quoted_hotel_logistics_amount", "quoted_accommodation_amount", "quoted_total_amount", "currency", "is_accommodation_provisional")
        }),
        ("Attribution & Ops Notes", {
            "fields": ("utm_source", "utm_medium", "utm_campaign", "utm_content", "internal_notes", "whatsapp_preview")
        }),
    )

    def whatsapp_preview(self, obj):
        if not obj.pk:
            return "Save lead first to preview message."
        return format_html('<pre style="white-space: pre-wrap; background: #EEF1FF; padding: 12px; border-radius: 8px;">{}</pre>', obj.generate_whatsapp_message())
    whatsapp_preview.short_description = "Formatted WhatsApp Message (§16.4)"

    def whatsapp_link(self, obj):
        url = obj.generate_whatsapp_url()
        return format_html('<a href="{}" target="_blank" style="color: #6750E8; font-weight: bold;">Open WhatsApp</a>', url)
    whatsapp_link.short_description = "WhatsApp"
