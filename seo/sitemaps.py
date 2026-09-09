from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from tours.models import Tour
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package
from content.models import GuideArticle

class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:prices',
            'core:plan_naivasha',
            'core:contact',
            'tours:tour_list',
            'partners:hotel_hub',
            'stays:stay_list',
            'packages:package_list',
            'bookings:book',
            'content:journal_list',
            'questions:faq_list',
        ]

    def location(self, item):
        return reverse(item)


class TourSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return Tour.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.verified_at


class HotelSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Strict gate: Only index hotel pages where marketing permission and public page are verified
        return HotelPartner.objects.filter(
            is_active=True,
            marketing_permission=True,
            public_page_enabled=True
        )

    def lastmod(self, obj):
        return obj.verified_at


class StaySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return AccommodationProperty.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.verified_at


class PackageSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Package.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.verified_at


class GuideSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return GuideArticle.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
