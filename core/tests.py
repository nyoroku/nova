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

    def test_i18n_set_language_swahili(self):
        set_resp = self.client.post(reverse('set_language'), {'language': 'sw', 'next': reverse('core:home')})
        self.assertEqual(set_resp.status_code, 302)
        resp = self.client.get(reverse('core:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Safari za Mashua")
        self.assertContains(resp, "Naivasha inaanzia hapa.")

    def test_all_10_languages_resolution(self):
        expected_translations = {
            'en': 'Boat Rides',
            'sw': 'Safari za Mashua',
            'fr': 'Balades en Bateau',
            'de': 'Bootsfahrten',
            'es': 'Paseos en Barco',
            'it': 'Giri in Barca',
            'zh-hans': '游船巡游',
            'ar': 'رحلات القوارب',
            'hi': 'नाव की सवारी',
            'nl': 'Boottochten',
        }
        for lang_code, expected_text in expected_translations.items():
            set_resp = self.client.post(reverse('set_language'), {'language': lang_code, 'next': reverse('core:home')})
            self.assertEqual(set_resp.status_code, 302, f"Failed redirect for {lang_code}")
            resp = self.client.get(reverse('core:home'))
            self.assertEqual(resp.status_code, 200, f"Failed status for {lang_code}")
            self.assertContains(resp, expected_text, msg_prefix=f"Language {lang_code} missing '{expected_text}'")
