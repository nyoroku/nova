from django.contrib import admin
from .models import (Tour, TourPriceTier, AddOn, ExperienceRate, TourOption, ActivityDetail,
                     ItineraryStep, ActivityFAQ, ActivityImage, ServiceIntent,
                     GBPService, GBPQueryScorecard, GBPPostTheme)
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
    list_display = (
        'name', 'effective_branded_name', 'effective_gbp_activity_name', 'status',
        'duration_minutes', 'google_activity_enabled', 'is_active',
        'readiness', 'gbp_url_preview', 'machine_endpoints', 'preview'
    )
    list_filter = ('status', 'category', 'is_active', 'google_activity_enabled')
    search_fields = ('name', 'branded_name', 'gbp_activity_name', 'primary_intent', 'summary', 'best_for')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OptionInline, ExperienceRateInline, DetailInline, ItineraryInline, FAQInline, ImageInline]
    readonly_fields = (
        'readiness', 'google_checklist', 'gbp_url_preview', 'machine_endpoints',
        'legacy_publication', 'legacy_body', 'duration_hours', 'capacity', 'updated_at', 'preview'
    )
    actions = ['publish_verified', 'pause_activities', 'run_consistency_audit']

    def readiness(self, obj):
        if not obj.pk:
            return 'Save as draft first.'
        issues = obj.publication_issues()
        return 'Ready' if not issues else '\n'.join(issues)

    def google_checklist(self, obj):
        return '\n'.join(obj.publication_issues(google=True)) if obj.pk else 'Save as draft first.'

    def gbp_url_preview(self, obj):
        if not obj.pk:
            return ''
        return format_html('<a href="{}" target="_blank" rel="noopener">GBP UTM URL</a>', obj.gbp_booking_url)

    def machine_endpoints(self, obj):
        if not obj.pk:
            return ''
        return format_html(
            '<a href="/activities/{}.json" target="_blank">JSON</a> · <a href="/activities/{}.md" target="_blank">MD</a>',
            obj.slug, obj.slug
        )

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

    @admin.action(description='Run canonical consistency & GBP readiness audit')
    def run_consistency_audit(self, request, queryset):
        from core.models import BusinessFact, ClaimEvidence
        stale_facts = [f.key for f in BusinessFact.objects.filter(active=True) if f.is_stale]
        stale_claims = [c.claim_key for c in ClaimEvidence.objects.filter(publishable=True) if c.is_stale]
        if stale_facts or stale_claims:
            self.message_user(
                request,
                f'Truth layer warning — stale facts: {stale_facts or "none"}; stale claims: {stale_claims or "none"}',
                level=messages.WARNING,
            )
        for tour in queryset:
            pub_issues = tour.publication_issues()
            gbp_issues = tour.publication_issues(google=True)
            if not pub_issues and not gbp_issues:
                self.message_user(request, f'{tour.name}: Web & Google Activities checklists passed.', level=messages.SUCCESS)
            else:
                detail = '; '.join(dict.fromkeys(pub_issues + gbp_issues))
                self.message_user(request, f'{tour.name}: {detail}', level=messages.WARNING)

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

@admin.register(GBPService)
class GBPServiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'primary_cluster', 'wave', 'activity', 'destination_url', 'is_active', 'last_verified_at')
    list_filter = ('primary_cluster', 'wave', 'is_active')
    search_fields = ('name', 'description')

@admin.register(GBPQueryScorecard)
class GBPQueryScorecardAdmin(admin.ModelAdmin):
    list_display = (
        'period_label', 'period_start', 'unique_discovery_queries',
        'lake_naivasha_boat_ride_searches', 'lake_naivasha_tour_searches',
        'crescent_island_searches', 'website_clicks', 'tracked_whatsapp_clicks',
        'gsc_ai_impressions', 'bing_ai_citations'
    )
    list_filter = ('period_start',)

@admin.register(GBPPostTheme)
class GBPPostThemeAdmin(admin.ModelAdmin):
    list_display = ('week_number', 'post_order', 'theme_title', 'target_cluster', 'activity', 'destination_url', 'is_active')
    list_filter = ('week_number', 'target_cluster', 'is_active')
    search_fields = ('theme_title', 'suggested_summary')



