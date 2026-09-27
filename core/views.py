from django.views.generic import TemplateView
from tours.models import Tour
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package
from content.models import Captain, QuestionAnswer, Testimonial, GuideArticle, ReviewSnapshot
from .models import SiteSettings

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings_obj = SiteSettings.get_solo()
        context['settings'] = settings_obj
        context['featured_tours'] = Tour.objects.filter(is_active=True).order_by('order')[:4]
        context['all_tours'] = Tour.objects.filter(is_active=True).order_by('order')
        context['hotel_partners'] = HotelPartner.objects.filter(is_active=True).prefetch_related('service_points')[:6]
        context['featured_stays'] = AccommodationProperty.objects.filter(is_active=True).order_by('order')[:3]
        context['featured_packages'] = Package.objects.filter(is_active=True).order_by('order')[:3]
        context['captain'] = Captain.objects.filter(is_active=True).first()
        context['captains'] = Captain.objects.filter(is_active=True).order_by('order')
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        context['quick_faqs'] = QuestionAnswer.objects.filter(is_active=True).order_by('order')[:8]
        context['latest_notes'] = GuideArticle.objects.filter(is_active=True).order_by('-published_at')[:4]
        context['review_snapshot'] = ReviewSnapshot.objects.filter(is_current=True).first()
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captains'] = Captain.objects.filter(is_active=True).order_by('order')
        return context


class PricesView(TemplateView):
    template_name = 'core/prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_solo()
        context['tours'] = Tour.objects.filter(is_active=True).prefetch_related('rates', 'price_tiers').order_by('order')
        context['packages'] = Package.objects.filter(is_active=True).order_by('order')
        from .models import ExternalFee
        from partners.models import HotelAccess
        context['crescent_fees'] = ExternalFee.objects.filter(
            is_active=True,
            provider_name__icontains='Crescent'
        ).order_by('id')
        context['all_external_fees'] = ExternalFee.objects.filter(is_active=True).order_by('provider_name', 'visitor_type')
        context['hotel_accesses'] = HotelAccess.objects.filter(is_published=True).select_related('property').order_by('property__order', 'property__name')
        context['review_snapshot'] = ReviewSnapshot.objects.filter(is_current=True).first()
        return context


class PlanNaivashaView(TemplateView):
    template_name = 'core/plan_naivasha.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planning_articles'] = GuideArticle.objects.filter(is_active=True).order_by('-published_at')
        return context

class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_solo()
        return context


class SitemapView(TemplateView):
    template_name = 'core/sitemap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tours'] = Tour.objects.filter(is_active=True).order_by('order')
        context['hotels'] = HotelPartner.objects.filter(
            is_active=True, marketing_permission=True, public_page_enabled=True
        )
        context['stays'] = AccommodationProperty.objects.filter(is_active=True).order_by('order')
        context['packages'] = Package.objects.filter(is_active=True).order_by('order')
        context['guides'] = GuideArticle.objects.filter(is_active=True).order_by('-published_at')
        context['faqs'] = QuestionAnswer.objects.filter(is_active=True).order_by('order')[:10]
        return context
