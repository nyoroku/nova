from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from partners.models import HotelPartner, HotelServicePoint

class PartnersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.public_partner = HotelPartner.objects.create(
            name="Enashipai Resort & Spa",
            slug="enashipai-resort-spa",
            marketing_permission=True,
            public_page_enabled=True,
            is_active=True
        )
        self.private_partner = HotelPartner.objects.create(
            name="Lake Naivasha Sopa Resort",
            slug="lake-naivasha-sopa-resort",
            marketing_permission=False,
            public_page_enabled=False,
            is_active=True
        )
        self.service_point = HotelServicePoint.objects.create(
            hotel=self.public_partner,
            name="Enashipai Main Jetty",
            service_mode="PARTNER_JETTY",
            public_instructions="Meet at the jetty.",
            notice_hours=2,
            is_active=True
        )

    def test_publication_gate_validation(self):
        # Cannot enable public page without marketing permission
        bad_partner = HotelPartner(
            name="Unverified Resort",
            slug="unverified-resort",
            marketing_permission=False,
            public_page_enabled=True
        )
        with self.assertRaises(ValidationError):
            bad_partner.clean()

    def test_hotel_hub_view(self):
        resp = self.client.get(reverse('partners:hotel_hub'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Enashipai Resort &amp; Spa")

    def test_public_hotel_detail(self):
        resp = self.client.get(reverse('partners:hotel_detail', kwargs={'slug': self.public_partner.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Enashipai Resort &amp; Spa")

    def test_sopa_gate_raises_404(self):
        resp = self.client.get(reverse('partners:hotel_detail', kwargs={'slug': self.private_partner.slug}))
        self.assertEqual(resp.status_code, 404)

    def test_hotel_checker_partial(self):
        url = reverse('partners:hotel_check')
        resp = self.client.get(f"{url}?hotel_id={self.public_partner.id}")
        self.assertContains(resp, "Direct Hotel Jetty Boarding")
