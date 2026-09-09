from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from tours.models import Tour, TourPriceTier

class ToursTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tour = Tour.objects.create(
            name="Classic Lake Safari",
            slug="classic-lake-safari",
            summary="A signature 1-hour boat safari",
            body="Detailed safari description",
            duration_hours=1.0,
            capacity=8,
            is_active=True
        )
        self.tier = TourPriceTier.objects.create(
            tour=self.tour,
            label="Standard Resident",
            resident_type="RESIDENT",
            pricing_unit="PER_PERSON",
            mode="SHARED",
            amount=Decimal("3000.00"),
            currency="KES",
            min_guests=1,
            max_guests=10,
            is_active=True
        )

    def test_tour_pricing_properties(self):
        self.assertEqual(self.tour.starting_price_resident, Decimal("3000.00"))
        self.assertEqual(self.tour.get_starting_price("RESIDENT"), Decimal("3000.00"))

    def test_tour_list_view(self):
        resp = self.client.get(reverse('tours:tour_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Classic Lake Safari")

    def test_tour_detail_view(self):
        resp = self.client.get(reverse('tours:tour_detail', kwargs={'slug': self.tour.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Classic Lake Safari")

    def test_tour_quote_partial(self):
        url = reverse('tours:quote_partial', kwargs={'slug': self.tour.slug})
        resp = self.client.get(f"{url}?adults=2&children=1&resident_type=RESIDENT")
        self.assertEqual(resp.status_code, 200)
        # 2 adults * 3000 = 6000 + 1 child * 1500 = 7500
        self.assertContains(resp, "7500")
