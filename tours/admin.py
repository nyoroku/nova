from django.contrib import admin
from .models import (Tour, TourPriceTier, AddOn, ExperienceRate, TourOption, ActivityDetail,
                     ItineraryStep, ActivityFAQ, ActivityImage, ServiceIntent)
from django.contrib import messages
from django.utils.html import format_html

class OptionInline(admin.StackedInline):
    model = TourOption
    extra = 0
    filter_horizontal = ('external_fees',)

class DetailInline(admin.TabularInline):
    model = ActivityDetail
    extra = 0

class ItineraryInline(admin.StackedInline):
    model = ItineraryStep
    extra = 0

class FAQInline(admin.StackedInline):
    model = ActivityFAQ
    extra = 0

class ImageInline(admin.StackedInline):
    model = ActivityImage
    extra = 0
    readonly_fields = ('width', 'height', 'content_hash', 'webp_image', 'webp_mobile')

class ExperienceRateInline(admin.TabularInline):
    model = ExperienceRate
    extra = 1

class TourPriceTierInline(admin.TabularInline):
    model = TourPriceTier
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'duration_minutes', 'operations_owner', 'is_active', 'readiness', 'preview')
    list_filter = ('status', 'category', 'is_active', 'google_activity_enabled')
    search_fields = ('name', 'summary', 'best_for')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OptionInline, ExperienceRateInline, DetailInline, ItineraryInline, FAQInline, ImageInline]
    readonly_fields = ('readiness', 'google_checklist', 'legacy_publication', 'legacy_body', 'duration_hours', 'capacity', 'updated_at', 'preview')
    actions = ['publish_verified', 'pause_activities']

    def readiness(self, obj):
        if not obj.pk:
            return 'Save as draft first.'
        issues = obj.publication_issues()
        return 'Ready' if not issues else '\n'.join(issues)

    def google_checklist(self, obj):
        return '\n'.join(obj.publication_issues(google=True)) if obj.pk else 'Save as draft first.'

    def preview(self, obj):
        return format_html('<a href="{}?preview=1">Preview activity</a>', obj.get_absolute_url()) if obj.pk else ''

    @admin.action(description='Publish activities that pass the complete checklist')
    def publish_verified(self, request, queryset):
        for tour in queryset:
            issues = tour.publication_issues()
            if issues:
                self.message_user(request, f'{tour.name}: ' + '; '.join(issues), level=messages.WARNING)
            else:
                tour.legacy_publication = False
                tour.status = 'PUBLISHED'
                tour.is_active = True
                tour.full_clean()
                tour.save()
                self.message_user(request, f'Published {tour.name}.')

    @admin.action(description='Pause selected activities')
    def pause_activities(self, request, queryset):
        queryset.update(status='PAUSED')

@admin.register(ExperienceRate)
class ExperienceRateAdmin(admin.ModelAdmin):
    list_display = ('experience', 'name', 'pricing_model', 'currency', 'amount', 'audience_type', 'is_active', 'is_public')
    list_filter = ('pricing_model', 'currency', 'audience_type', 'is_active', 'is_public')
    search_fields = ('experience__name', 'name')
    list_select_related = ('experience', 'option')

@admin.register(TourPriceTier)
class TourPriceTierAdmin(admin.ModelAdmin):
    list_display = ('tour', 'label', 'resident_type', 'mode', 'amount', 'currency', 'is_active')
    list_filter = ('resident_type', 'mode', 'currency', 'is_active')
    search_fields = ('tour__name', 'label')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_mode', 'amount', 'currency', 'is_active')
    list_filter = ('price_mode', 'currency', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(TourOption)
class TourOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'tour', 'mode', 'duration_minutes', 'min_guests', 'max_guests', 'verified_at', 'is_active')
    filter_horizontal = ('external_fees',)
    list_filter = ('mode', 'is_active')

@admin.register(ServiceIntent)
class ServiceIntentAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category', 'activity', 'operational_verified_at', 'is_active')
    list_filter = ('level', 'category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

