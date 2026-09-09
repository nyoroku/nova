from django.contrib import admin
from .models import Package, PackageComponent

class PackageComponentInline(admin.TabularInline):
    model = PackageComponent
    extra = 2

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_days', 'duration_nights', 'starting_price', 'currency', 'is_featured', 'is_active', 'verified_at')
    list_filter = ('is_featured', 'is_active', 'includes_hotel_origin_pickup', 'includes_crescent_island')
    search_fields = ('name', 'tagline', 'summary')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('eligible_tours', 'accommodation_properties')
    inlines = [PackageComponentInline]
