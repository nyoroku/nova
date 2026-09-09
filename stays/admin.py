from django.contrib import admin
from .models import AccommodationProperty, RoomType, AccommodationRate

class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1

class AccommodationRateInline(admin.TabularInline):
    model = AccommodationRate
    extra = 1

@admin.register(AccommodationProperty)
class AccommodationPropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'inventory_mode', 'starting_price', 'currency', 'is_featured', 'is_active', 'verified_at')
    list_filter = ('inventory_mode', 'property_type', 'is_featured', 'is_active')
    search_fields = ('name', 'summary', 'address')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoomTypeInline]

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'max_adults', 'max_children', 'bed_configuration', 'is_active')
    list_filter = ('property', 'is_active')
    inlines = [AccommodationRateInline]

@admin.register(AccommodationRate)
class AccommodationRateAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'meal_plan', 'pricing_mode', 'resident_type', 'amount', 'currency', 'is_available', 'verified_at')
    list_filter = ('meal_plan', 'pricing_mode', 'resident_type', 'is_available')
