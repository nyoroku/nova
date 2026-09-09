from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import GuideArticle, QuestionAnswer, Captain

class JournalListView(ListView):
    model = GuideArticle
    template_name = 'content/journal_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        qs = GuideArticle.objects.filter(is_active=True).order_by('-is_featured', '-published_at')
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GuideArticle.CATEGORY_CHOICES
        context['current_cat'] = self.request.GET.get('category', '')
        return context


class JournalDetailView(DetailView):
    model = GuideArticle
    template_name = 'content/journal_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        return get_object_or_404(GuideArticle, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = GuideArticle.objects.filter(is_active=True).exclude(pk=self.object.pk)[:3]
        return context


class FAQView(ListView):
    model = QuestionAnswer
    template_name = 'content/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return QuestionAnswer.objects.filter(is_active=True).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = QuestionAnswer.CATEGORY_CHOICES
        return context
