from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from stays.models import AccommodationProperty, RoomType

class StaysTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.property = AccommodationProperty.objects.create(
            name="Kiboko Luxury Camp",
            slug="kiboko-luxury-camp",
            property_type="CAMP",
            inventory_mode="ALLOTMENT",
            address="South Lake Road",
            starting_price=Decimal("35000.00"),
            summary="Luxury tented camp directly on Lake Naivasha shore",
            description="Detailed luxury camp description",
            is_active=True
        )
        self.room = RoomType.objects.create(
            property=self.property,
            name="Lake-Facing Tent",
            max_adults=2,
            max_children=0,
            is_active=True
        )

    def test_stay_list_view(self):
        resp = self.client.get(reverse('stays:stay_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Kiboko Luxury Camp")

    def test_stay_detail_view(self):
        resp = self.client.get(reverse('stays:stay_detail', kwargs={'slug': self.property.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Lake-Facing Tent")
