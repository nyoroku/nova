from django.contrib import admin
from .models import Captain, GuideArticle, QuestionAnswer, Testimonial

@admin.register(Captain)
class CaptainAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_title', 'years_on_lake', 'is_active', 'order')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GuideArticle)
class GuideArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'is_active', 'verified_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_featured', 'is_active', 'order', 'verified_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('question', 'answer')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_segment', 'rating', 'trip_date', 'is_featured', 'is_active')
    list_filter = ('guest_segment', 'rating', 'is_featured', 'is_active')
    search_fields = ('guest_name', 'text')
