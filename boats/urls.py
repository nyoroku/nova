# boats/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap, index as sitemap_index
from seo.sitemaps import StaticViewSitemap, TourSitemap, HotelSitemap, StaySitemap, PackageSitemap, GuideSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'tours': TourSitemap,
    'hotels': HotelSitemap,
    'stays': StaySitemap,
    'packages': PackageSitemap,
    'guides': GuideSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Nova Primary Architecture (§9)
    path('', include('core.urls')),
    path('boat-rides/', include('tours.urls')),
    path('hotel-boat-rides/', include('partners.urls')),
    path('stay/', include('stays.urls')),
    path('packages/', include('packages.urls')),
    path('book/', include('bookings.urls')),
    path('journal/', include('content.urls')),
    path('questions/', include('content.faq_urls')),

    # 301 Redirects for Legacy Paths
    path('tours/', RedirectView.as_view(url='/boat-rides/', permanent=True)),
    path('accommodation/', RedirectView.as_view(url='/stay/', permanent=True)),
    path('reviews/', RedirectView.as_view(url='/about/', permanent=True)),
    path('faq/', RedirectView.as_view(url='/questions/', permanent=True)),

    path("tinymce/", include("tinymce.urls")),
    path('', include('seo.urls')),

    # Sitemaps
    path('sitemap.xml', sitemap_index, {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemap_section'}, name='sitemap'),
    path('sitemap_index.xml', sitemap_index, {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemap_section'}, name='sitemap_index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap_section'),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
