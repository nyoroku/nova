from django.test import TestCase, Client
from django.urls import reverse
from content.models import Captain, GuideArticle, QuestionAnswer, Testimonial

class ContentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.captain = Captain.objects.create(
            name="Captain Dennis Maina",
            slug="dennis-maina",
            role_title="Lead Lake Captain",
            years_on_lake=12,
            bio="Experienced lake captain.",
            is_active=True
        )
        self.article = GuideArticle.objects.create(
            title="Best Time for Boat Ride",
            slug="best-time-boat-ride",
            excerpt="Morning vs afternoon lake dynamics",
            body="<p>Morning is calm.</p>",
            category="WILDLIFE",
            is_active=True
        )
        self.faq = QuestionAnswer.objects.create(
            question="Are life jackets provided?",
            answer="Yes, certified life jackets are mandatory.",
            category="SAFETY",
            is_active=True
        )

    def test_journal_list_view(self):
        resp = self.client.get(reverse('content:journal_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Best Time for Boat Ride")

    def test_journal_detail_view(self):
        resp = self.client.get(reverse('content:journal_detail', kwargs={'slug': self.article.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Morning is calm.")

    def test_faq_list_view(self):
        resp = self.client.get(reverse('questions:faq_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Are life jackets provided?")
