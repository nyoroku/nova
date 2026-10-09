import json
from datetime import timedelta
from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from PIL import Image
from bs4 import BeautifulSoup
from .models import Tour, TourOption, ExperienceRate, TourPriceTier, ActivityImage
from .pricing import quote_activity
from .attribution import campaign_url
from core.models import ExternalFee
from partners.models import HotelPartner, HotelAccess


class PricingAndCatalogueTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.tour = Tour.objects.create(name='Test lake ride', slug='test-lake-ride', summary='A lake introduction',
            body='Our lake experience.', status='PUBLISHED', legacy_publication=True, duration_minutes=60)
        self.option = TourOption.objects.create(tour=self.tour, name='Private hour', mode='PRIVATE', duration_minutes=60,
            min_guests=1, max_guests=7)
        self.rate = ExperienceRate.objects.create(experience=self.tour, option=self.option, name='Private hour KES',
            pricing_model='PER_BOAT', currency='KES', amount=Decimal('4500'), min_guests=1, max_guests=7,
            duration_minutes=60, effective_from=self.today)
        TourPriceTier.objects.create(tour=self.tour, label='Legacy', amount=16000, currency='KES')

    def quote(self, **kwargs):
        return quote_activity(self.tour, option_id=self.option.pk, **kwargs)

    def test_private_price_is_not_multiplied_by_passengers(self):
        self.assertEqual(self.quote(adults=5, children=2).total, Decimal('4500'))

    def test_no_legacy_or_numeric_fallback(self):
        self.rate.is_active = False; self.rate.save()
        self.assertIsNone(self.quote().total)
        self.assertIsNone(self.tour.get_starting_price())

    def test_effective_date_is_the_service_date(self):
        self.rate.effective_until = self.today; self.rate.save()
        self.assertTrue(self.quote(service_date=self.today).complete)
        self.assertFalse(self.quote(service_date=self.today + timedelta(days=1)).complete)

    def test_future_and_overlapping_rates_do_not_silently_win(self):
        self.rate.effective_from = self.today + timedelta(days=7); self.rate.save()
        self.assertFalse(self.quote().complete)
        self.rate.effective_from = self.today; self.rate.save()
        ExperienceRate.objects.create(experience=self.tour, option=self.option, name='Overlapping', amount=4000,
            duration_minutes=60, min_guests=1, max_guests=7, effective_from=self.today)
        self.assertFalse(self.quote().complete)

    def test_capacity_and_duration_are_enforced(self):
        self.assertFalse(self.quote(adults=8).complete)
        self.rate.duration_minutes = 120; self.rate.save()
        self.assertFalse(self.quote().complete)
        with self.assertRaises(ValidationError): self.rate.full_clean()

    def test_child_discount_must_be_explicit(self):
        self.rate.pricing_model = 'PER_PERSON'; self.rate.amount = 1500; self.rate.save()
        self.assertFalse(self.quote(adults=2, children=1).complete)
        self.rate.child_amount = 800; self.rate.save()
        self.assertEqual(self.quote(adults=2, children=1).total, Decimal('3800'))

    def test_multiple_options_require_selection(self):
        TourOption.objects.create(tour=self.tour, name='Longer ride', mode='PRIVATE', duration_minutes=120, max_guests=7)
        self.assertFalse(quote_activity(self.tour).complete)
        self.assertTrue(self.quote().complete)

    def test_external_admission_included_in_total_but_itemized(self):
        fee = ExternalFee.objects.create(provider_name='Test island',service_name='Entry', visitor_type='RESIDENT',
            adult_amount=1000, child_amount=500, currency='KES', effective_from=self.today, last_verified_at=self.today)
        self.option.external_fees.add(fee)
        quote = self.quote(adults=2)
        self.assertEqual(quote.total, Decimal('6500'))
        self.assertEqual(quote.lines[-1]['pay_to'], 'Attraction provider')
        self.assertFalse(self.quote(adults=2, children=1).complete)
        fee.effective_until = self.today - timedelta(days=1); fee.save()
        self.assertFalse(self.quote().complete)

    def test_hotel_fee_comes_from_configuration_and_no_exchange_is_assumed(self):
        hotel = HotelPartner.objects.create(name='Test property',slug='test-property')
        access = HotelAccess.objects.create(property=hotel, positioning_fee=1750, currency='KES',
            last_verified_at=self.today, verification_evidence='Confirmed test access',
            is_published=True, access_mode='DIRECT_JETTY', access_status='VERIFIED_ACTIVE')
        self.assertEqual(self.quote(adults=2,hotel=hotel).total,Decimal('6250'))
        access.access_mode='ROAD_TRANSFER'; access.save()
        self.assertFalse(self.quote(hotel=hotel).complete)
        self.assertFalse(self.quote(currency='USD').complete)

    def test_draft_and_paused_products_are_absent_from_routes_and_sitemaps(self):
        self.tour.status = 'DRAFT'; self.tour.save()
        self.assertEqual(self.client.get(self.tour.get_absolute_url()).status_code,404)
        self.assertNotContains(self.client.get('/boat-rides/'),self.tour.name)
        self.assertNotContains(self.client.get('/sitemap.xml'),self.tour.get_absolute_url())
        self.tour.status = 'PAUSED'; self.tour.save()
        self.assertEqual(self.client.get(self.tour.get_absolute_url()).status_code,404)
        self.tour.status='PUBLISHED'
        with self.assertRaises(ValidationError): self.tour.full_clean()

    def test_staff_preview_is_noindex(self):
        self.tour.status='DRAFT'; self.tour.save()
        user=get_user_model().objects.create_user('preview',password='test-pass',is_staff=True)
        from django.contrib.auth.models import Permission
        user.user_permissions.add(Permission.objects.get(codename='view_tour'))
        self.client.force_login(user)
        response=self.client.get(self.tour.get_absolute_url()+'?preview=1')
        self.assertContains(response,'noindex, nofollow')

    def test_schema_canonical_and_one_h1(self):
        self.tour.name='Ride "special" <script>'; self.tour.save()
        response=self.client.get(self.tour.get_absolute_url()+'?utm_source=google&utm_campaign=gbp_activities')
        soup=BeautifulSoup(response.content,'html.parser')
        self.assertEqual(len(soup.find_all('h1')),1)
        self.assertEqual(soup.find('link',rel='canonical')['href'],self.tour.canonical_url)
        for script in soup.find_all('script',type='application/ld+json'): json.loads(script.string)
        self.assertContains(response,'per boat')
        self.assertNotContains(response,'16000')

    def test_export_urls_are_consistent_and_internal_links_are_clean(self):
        url=campaign_url(self.tour.canonical_url+'?utm_campaign=old','activity',self.tour.slug)
        self.assertIn('utm_campaign=gbp_activities',url)
        self.assertIn('utm_content=test-lake-ride',url)
        soup=BeautifulSoup(self.client.get('/boat-rides/').content,'html.parser')
        self.assertFalse(any('utm_' in a.get('href','') for a in soup.find_all('a')))
        self.assertTrue(self.tour.publication_issues(google=True))

    def test_primary_image_uniqueness_and_optimized_gallery_markup(self):
        with TemporaryDirectory(prefix='nova-test-images-') as media, override_settings(MEDIA_ROOT=media):
            for index in range(6):
                stream=BytesIO(); Image.new('RGB',(1800,1200),(index*30,100,120)).save(stream,'JPEG')
                ActivityImage.objects.create(tour=self.tour,image=SimpleUploadedFile(f'test-{index}.jpg',stream.getvalue(),content_type='image/jpeg'),
                    alt_text=f'Test fixture photo {index}',is_primary=index==0,rights_confirmed=True,display_order=index)
            image=self.tour.images.get(is_primary=True)
            self.assertEqual((image.width,image.height),(1800,1200))
            with Image.open(image.webp_image.path) as optimized: self.assertLessEqual(optimized.width,1280)
            with self.assertRaises(IntegrityError), transaction.atomic():
                ActivityImage.objects.create(tour=self.tour,image=image.image.name,alt_text='Duplicate',is_primary=True)
            soup=BeautifulSoup(self.client.get(self.tour.get_absolute_url()).content,'html.parser')
            pictures=soup.select('.activity-gallery-track img')
            self.assertEqual(len(pictures),6)
            self.assertEqual(pictures[0].get('fetchpriority'),'high')
            self.assertTrue(all(i.get('loading')=='lazy' for i in pictures[1:]))
            self.assertTrue(all(i.get('alt') and i.get('width') and i.get('height') for i in pictures))

    def test_existing_slugs_and_ten_record_plan(self):
        slugs=['classic-lake-safari','hippo-bird-safari','crescent-island','sunset-cruise','private-charter','family-ride','photography-birding','groups-events','sunrise-wildlife','full-lake-explorer']
        self.assertEqual(Tour.objects.filter(slug__in=slugs).count(),10)
        self.assertEqual(Tour.objects.get(slug='sunrise-wildlife').status,'DRAFT')
        self.assertEqual(Tour.objects.get(slug='full-lake-explorer').status,'DRAFT')

    def test_group_minimum_transaction_cost(self):
        self.option.min_guests=10; self.option.max_guests=30; self.option.mode='GROUP'; self.option.save()
        self.rate.min_guests=10; self.rate.max_guests=30; self.rate.pricing_model='PER_PERSON'; self.rate.amount=1200; self.rate.save()
        self.assertFalse(self.quote(adults=2).complete)
        self.assertEqual(self.rate.minimum_total,Decimal('12000'))
        self.assertEqual(self.quote(adults=10).total,Decimal('12000'))

    def test_services_map_to_real_destinations_without_thin_pages(self):
        from .models import ServiceIntent
        self.assertEqual(ServiceIntent.objects.count(),30)
        self.assertEqual(ServiceIntent.objects.filter(level='PRIMARY').count(),15)
        self.assertEqual(ServiceIntent.objects.filter(level='SECONDARY').count(),15)
        self.assertEqual(self.client.get('/services/').status_code,200)
        self.assertEqual(self.client.get('/services/boat-ride-on-lake-naivasha/').status_code,404)

    def test_unverified_publication_is_rejected(self):
        draft=Tour.objects.get(slug='sunrise-wildlife')
        draft.status='PUBLISHED'
        with self.assertRaises(ValidationError): draft.full_clean()
        self.assertIn('Confirm operational facts, evidence and responsible owner.',draft.publication_issues())

    def test_custom_quote_is_not_advertised_as_a_fixed_price(self):
        self.rate.pricing_model='CUSTOM_QUOTE'; self.rate.save()
        response=self.client.get(self.tour.get_absolute_url())
        self.assertContains(response,'Request an individual quote')
        self.assertNotContains(response,'KES 4500')
