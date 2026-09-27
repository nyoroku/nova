from django.contrib import admin
from .models import Captain, GuideArticle, QuestionAnswer, Testimonial, ReviewSnapshot, ArticleSource

@admin.register(Captain)
class CaptainAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_title', 'years_on_lake', 'certification_text', 'is_active', 'order')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


class ArticleSourceInline(admin.TabularInline):
    model = ArticleSource
    extra = 1


@admin.register(GuideArticle)
class GuideArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_featured', 'is_active', 'verified_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleSourceInline]


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


@admin.register(ReviewSnapshot)
class ReviewSnapshotAdmin(admin.ModelAdmin):
    list_display = ('source', 'rating', 'review_count', 'captured_at', 'is_current')
    list_filter = ('source', 'is_current')


@admin.register(ArticleSource)
class ArticleSourceAdmin(admin.ModelAdmin):
    list_display = ('article', 'source_name', 'source_type', 'verified_at', 'display_publicly')
    list_filter = ('source_type', 'display_publicly')
    search_fields = ('article__title', 'source_name', 'claim_supported')

