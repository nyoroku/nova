from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import FAQ, LocalPage


def robots_txt(request):
    """Publish crawler directives from the same canonical origin as the site."""
    body = "\n".join([
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /accounts/",
        "Disallow: /tinymce/",
        f"Sitemap: {settings.SITE_URL}/sitemap_index.xml",
        "",
    ])
    return HttpResponse(body, content_type='text/plain; charset=utf-8')


class FAQView(ListView):
    model = FAQ
    template_name = 'seo/faq.html'
    context_object_name = 'faqs'
    paginate_by = 20  # Improves crawlability for large FAQ sets

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "meta_title": "Frequently Asked Questions | Lake Naivasha Boat Rides",
            "meta_description": "Answers to common questions about boat rides in Lake Naivasha, Crescent Island tours, hippo safaris, safety, pricing, and bookings.",
            "canonical_url": self.request.build_absolute_uri(),
            "last_updated": FAQ.objects.filter(is_active=True).latest("updated_at").updated_at,
            "schema_type": "FAQPage",  # Used in template for JSON-LD
        })

        return context


class LocalPageListView(ListView):
    model = LocalPage
    template_name = 'seo/list.html'
    context_object_name = 'pages'
    paginate_by = 24

    def get_queryset(self):
        return LocalPage.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "meta_title": "Boat Rides & Tours in Lake Naivasha | Nova Boat Rides",
            "meta_description": "Explore boat rides, Crescent Island tours, hippo safaris, sunset cruises, and family-friendly experiences on Lake Naivasha.",
            "canonical_url": self.request.build_absolute_uri(),
        })

        return context


class LocalPageDetailView(DetailView):
    model = LocalPage
    template_name = 'seo/detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return LocalPage.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_pages = LocalPage.objects.filter(
            is_active=True
        ).exclude(id=self.object.id)[:6]

        context.update({
            "meta_title": self.object.title,
            "meta_description": self.object.meta_description,
            "canonical_url": self.request.build_absolute_uri(),
            "last_updated": self.object.updated_at,
            "related_pages": related_pages,  # Internal linking boost
            "schema_type": "Article",  # Or LocalBusiness
        })

        return context

