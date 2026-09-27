from django.contrib import admin
from .models import Tour, TourPriceTier, AddOn, ExperienceRate

class ExperienceRateInline(admin.TabularInline):
    model = ExperienceRate
    extra = 1

class TourPriceTierInline(admin.TabularInline):
    model = TourPriceTier
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_hours', 'capacity', 'is_featured', 'is_active', 'verified_at')
    list_filter = ('is_active', 'is_featured', 'is_private', 'is_shared')
    search_fields = ('name', 'summary', 'best_for')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExperienceRateInline, TourPriceTierInline]

@admin.register(ExperienceRate)
class ExperienceRateAdmin(admin.ModelAdmin):
    list_display = ('experience', 'name', 'pricing_model', 'currency', 'amount', 'audience_type', 'is_active', 'is_public')
    list_filter = ('pricing_model', 'currency', 'audience_type', 'is_active', 'is_public')
    search_fields = ('experience__name', 'name')

@admin.register(TourPriceTier)
class TourPriceTierAdmin(admin.ModelAdmin):
    list_display = ('tour', 'label', 'resident_type', 'mode', 'amount', 'currency', 'is_active')
    list_filter = ('resident_type', 'mode', 'currency', 'is_active')
    search_fields = ('tour__name', 'label')

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_mode', 'amount', 'currency', 'is_active')
    list_filter = ('price_mode', 'currency', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

