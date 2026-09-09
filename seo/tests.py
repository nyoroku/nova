from django.test import TestCase, Client
from seo.models import Redirect

class SEOTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Redirect.objects.create(
            old_path="/old-crescent-tour",
            new_path="/boat-rides/crescent-island/",
            status_code=301,
            is_active=True
        )

    def test_robots_txt(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("User-agent: *", resp.content.decode('utf-8'))
        self.assertIn("Sitemap:", resp.content.decode('utf-8'))

    def test_custom_redirect_middleware(self):
        resp = self.client.get('/old-crescent-tour')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp.url, '/boat-rides/crescent-island/')

    def test_legacy_301_redirects(self):
        resp = self.client.get('/tours/')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp.url, '/boat-rides/')
