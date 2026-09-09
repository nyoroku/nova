from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from bookings.models import BookingLead
from tours.models import Tour, TourPriceTier

class BookingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tour = Tour.objects.create(
            name="Hippo Safari",
            slug="hippo-safari",
            summary="Hippo Safari",
            is_active=True
        )
        TourPriceTier.objects.create(
            tour=self.tour,
            label="Std",
            resident_type="RESIDENT",
            pricing_unit="PER_PERSON",
            mode="SHARED",
            amount=Decimal("3000.00"),
            currency="KES",
            is_active=True
        )

    def test_whatsapp_message_format(self):
        lead = BookingLead.objects.create(
            lead_type='BOAT_ONLY',
            tour=self.tour,
            guest_name='John Doe',
            guest_phone='+254700112233',
            preferred_date='2026-09-12',
            preferred_time='Morning (08:30)',
            adults=2,
            children=1,
            quoted_boat_amount=Decimal("7500.00"),
            quoted_total_amount=Decimal("7500.00"),
            consent_operational=True
        )
        msg = lead.generate_whatsapp_message()
        self.assertIn("Hi Nova.", msg)
        self.assertIn("Hippo Safari", msg)
        self.assertIn("KES 7,500", msg)
        self.assertIn(lead.reference, msg)

    def test_book_view_get(self):
        resp = self.client.get(reverse('bookings:book'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Reservation Request")

    def test_book_view_post_htmx(self):
        post_data = {
            'lead_type': 'BOAT_ONLY',
            'tour': self.tour.pk,
            'preferred_date': '2026-09-15',
            'preferred_time': 'MORNING_0830',
            'adults': 2,
            'children': 0,
            'transport_required': 'NONE',
            'guest_name': 'Sarah Doe',
            'guest_phone': '+254711223344',
            'guest_email': 'sarah@example.com',
            'consent_operational': True,
        }
        resp = self.client.post(reverse('bookings:book'), post_data, HTTP_HX_REQUEST='true')
        self.assertContains(resp, "Almost on the Water")
        
        lead = BookingLead.objects.filter(guest_name='Sarah Doe').first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.quoted_total_amount, Decimal("6000.00"))
