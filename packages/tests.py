from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from packages.models import Package, PackageComponent
from tours.models import Tour, TourPriceTier
from stays.models import AccommodationProperty

class PackagesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.tour = Tour.objects.create(
            name="Classic Safari",
            slug="classic-safari",
            summary="Safari",
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
        self.stay = AccommodationProperty.objects.create(
            name="Lakeside Haven",
            slug="lakeside-haven",
            inventory_mode="ALLOTMENT",
            starting_price=Decimal("15000.00"),
            is_active=True
        )
        self.package = Package.objects.create(
            name="Stay and Ride Classic",
            slug="stay-and-ride-classic",
            tagline="1 Night stay and morning boat safari",
            duration_nights=1,
            duration_days=2,
            starting_price=Decimal("21000.00"),
            includes_hotel_origin_pickup=True,
            is_active=True
        )
        self.package.eligible_tours.add(self.tour)
        self.package.accommodation_properties.add(self.stay)
        PackageComponent.objects.create(
            package=self.package,
            title="Sunrise Boat Safari",
            component_type="BOAT"
        )

    def test_package_list_view(self):
        resp = self.client.get(reverse('packages:package_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Stay and Ride Classic")

    def test_package_detail_view(self):
        resp = self.client.get(reverse('packages:package_detail', kwargs={'slug': self.package.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sunrise Boat Safari")

    def test_package_quote_partial(self):
        url = reverse('packages:quote_partial', kwargs={'slug': self.package.slug})
        resp = self.client.get(f"{url}?adults=2&children=0&stay_id={self.stay.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "23000")
