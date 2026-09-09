from django.test import TestCase, Client
from django.urls import reverse
from core.models import SiteSettings

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.get_solo()
        self.settings.business_name = "Nova Boat Rides Naivasha"
        self.settings.save()

    def test_home_view(self):
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Nova")

    def test_about_view(self):
        resp = self.client.get(reverse('core:about'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "About Nova")

    def test_prices_view(self):
        resp = self.client.get(reverse('core:prices'))
        self.assertEqual(resp.status_code, 200)

    def test_plan_naivasha_view(self):
        resp = self.client.get(reverse('core:plan_naivasha'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Plan Your Naivasha Experience")

    def test_contact_view(self):
        resp = self.client.get(reverse('core:contact'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Find Nova on Lake Naivasha")
