"""
seed_truth_layer.py
Canonical Truth Layer Seeder for Nova Boat Rides Naivasha.
Ensures single source of truth across pricing, external fees, hotel access,
and captain credentials.
"""
import os
import django
from decimal import Decimal
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.utils import timezone
from core.models import SiteSettings, ExternalFee
from tours.models import Tour, TourPriceTier, ExperienceRate
from partners.models import HotelPartner, HotelAccess
from content.models import Captain, ReviewSnapshot, ArticleSource, GuideArticle


def seed_site_settings():
    print("--- Seeding SiteSettings ---")
    settings, created = SiteSettings.objects.get_or_create(id=1)
    settings.business_name = "Nova Boat Rides Naivasha"
    settings.legal_name = "Nova Boat Rides Naivasha Ltd"
    settings.tagline = "Naivasha starts here."
    settings.supporting_proposition = "Direct boat tours, Crescent Island transfers, and private charters on Lake Naivasha. Depart from Nova Karagita Base or selected partner hotel jetties."
    settings.phone_display = "+254 701 215 295"
    settings.phone_e164 = "+254701215295"
    settings.whatsapp_number = "254701215295"
    settings.email = "hello@novaboatridesnaivasha.co.ke"
    settings.street_address = "Karagita Beach, Moi South Lake Road"
    settings.locality = "Karagita, Naivasha"
    settings.county = "Nakuru County"
    settings.country = "Kenya"
    settings.standard_launch_name = "Nova Karagita Base, Lake Naivasha"
    settings.standard_launch_lat = Decimal("-0.762030")
    settings.standard_launch_lng = Decimal("36.425790")
    settings.opening_time = "06:30"
    settings.closing_time = "18:30"
    settings.operating_hours = "Daily 6:30 AM – 6:30 PM (Last boat launch 5:30 PM)"
    settings.default_currency = "KES"
    settings.google_maps_url = "https://maps.google.com/?q=-0.762030,36.425790"
    settings.google_business_profile_url = "https://maps.app.goo.gl/wYv8x5V5o6H3o1Rk8"
    settings.gbp_url = "https://maps.app.goo.gl/wYv8x5V5o6H3o1Rk8"
    settings.directions_summary = (
        "Located at Karagita Beach off Moi South Lake Road, Naivasha (8 km south of Naivasha Town). "
        "Dedicated briefing pavilion, secure perimeter parking, life jacket fitting station, and direct boat jetty access."
    )
    settings.booking_notice = (
        "Advance booking recommended for morning and sunset departures, hotel jetty pickups, and Crescent Island walking tours. "
        "Same-day walk-ins welcome at Karagita Base subject to boat and captain availability."
    )
    settings.save()
    print("SiteSettings saved successfully.")


def seed_external_fees():
    print("--- Seeding External Fees ---")
    today = timezone.now().date()
    
    fees = [
        {
            'provider_name': "Crescent Island Game Sanctuary",
            'service_name': "Sanctuary Walking Conservation Fee (Kenyan Citizen Adult)",
            'visitor_type': 'CITIZEN',
            'adult_amount': Decimal("800.00"),
            'child_amount': Decimal("400.00"),
            'student_amount': None,
            'currency': 'KES',
            'source_url': "https://www.crescentisland.co/",
            'source_name': "Crescent Island Game Sanctuary Official Schedule",
            'notes': "Paid directly to Crescent Island Sanctuary at gate (cashless/card/M-Pesa). Covers guided walking safari.",
        },
        {
            'provider_name': "Crescent Island Game Sanctuary",
            'service_name': "Sanctuary Walking Conservation Fee (East African Resident Adult)",
            'visitor_type': 'RESIDENT',
            'adult_amount': Decimal("1100.00"),
            'child_amount': Decimal("550.00"),
            'student_amount': None,
            'currency': 'KES',
            'source_url': "https://www.crescentisland.co/",
            'source_name': "Crescent Island Game Sanctuary Official Schedule",
            'notes': "Proof of residency required. Paid directly at gate.",
        },
        {
            'provider_name': "Crescent Island Game Sanctuary",
            'service_name': "Sanctuary Walking Conservation Fee (Non-Resident / International)",
            'visitor_type': 'NON_RESIDENT',
            'adult_amount': Decimal("33.00"),
            'child_amount': Decimal("16.00"),
            'student_amount': Decimal("22.00"),
            'currency': 'USD',
            'source_url': "https://www.crescentisland.co/",
            'source_name': "Crescent Island Game Sanctuary Official Schedule",
            'notes': "International visitors pay in USD or equivalent via card/cashless at sanctuary entrance.",
        },
        {
            'provider_name': "Kenya Wildlife Service",
            'service_name': "Hell's Gate National Park Conservation Entry",
            'visitor_type': 'CITIZEN',
            'adult_amount': Decimal("300.00"),
            'child_amount': Decimal("215.00"),
            'student_amount': None,
            'currency': 'KES',
            'source_url': "https://www.kws.go.ke/",
            'source_name': "KWS Conservation Tariff",
            'notes': "For combination multi-adventure day trips. Paid via eCitizen platform.",
        },
        {
            'provider_name': "Kenya Wildlife Service",
            'service_name': "Hell's Gate National Park Conservation Entry (Non-Resident)",
            'visitor_type': 'NON_RESIDENT',
            'adult_amount': Decimal("26.00"),
            'child_amount': Decimal("17.00"),
            'student_amount': None,
            'currency': 'USD',
            'source_url': "https://www.kws.go.ke/",
            'source_name': "KWS Conservation Tariff",
            'notes': "International conservation entry fee via eCitizen platform.",
        },
    ]

    for item in fees:
        fee, created = ExternalFee.objects.update_or_create(
            provider_name=item['provider_name'],
            service_name=item['service_name'],
            visitor_type=item['visitor_type'],
            defaults={
                'adult_amount': item['adult_amount'],
                'child_amount': item['child_amount'],
                'student_amount': item['student_amount'],
                'currency': item['currency'],
                'source_url': item['source_url'],
                'source_name': item['source_name'],
                'last_verified_at': today,
                'is_active': True,
                'notes': item['notes'],
            }
        )
        print(f"ExternalFee: {fee}")


def seed_experience_rates():
    print("--- Seeding Experience Rates & Updating Price Tiers ---")
    today = timezone.now().date()

    tours_rates = {
        'classic-lake-safari': [
            {
                'name': "1-Hour Private Boat Charter (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("4500.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 60,
                'notes': "Entire boat for your private group of up to 7 passengers. Professional captain guide, fuel, and life jackets included.",
            },
            {
                'name': "1-Hour Private Boat Charter - USD (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("45.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 60,
                'notes': "Private boat charter for international travelers. Certified captain, life jackets, and safety gear included.",
            },
            {
                'name': "Shared Boat Seat (Per Person)",
                'pricing_model': 'PER_PERSON',
                'currency': 'KES',
                'amount': Decimal("1500.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 60,
                'notes': "Available for solo travelers or small parties joining scheduled departures from Karagita Base.",
            },
            {
                'name': "Shared Boat Seat - USD (Per Person)",
                'pricing_model': 'PER_PERSON',
                'currency': 'USD',
                'amount': Decimal("20.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 60,
                'notes': "Shared seat rate for international visitors.",
            },
        ],
        'crescent-island': [
            {
                'name': "Private Boat Transfer & Return Standby (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("6500.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 150,
                'notes': "Includes scenic boat ride across Lake Naivasha, captain standby while you explore the sanctuary on foot, and return journey. Sanctuary entrance fee paid separately at gate.",
            },
            {
                'name': "Private Boat Transfer & Return Standby - USD (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("65.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 150,
                'notes': "Boat transfer, captain standby, return voyage for international visitors. Sanctuary entrance fees payable at gate (USD 33 adult / USD 16 child).",
            },
        ],
        'sunset-cruise': [
            {
                'name': "1.5-Hour Private Sunset Cruise (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("7000.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 90,
                'notes': "Golden-hour navigation timed for optimal lighting, calm water, and hippo pool viewing. Departs 4:30 PM - 5:00 PM.",
            },
            {
                'name': "1.5-Hour Private Sunset Cruise - USD (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("70.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 90,
                'notes': "Golden-hour cruise for international guests.",
            },
        ],
        'hippo-bird-safari': [
            {
                'name': "2-Hour Hippo & Bird Watching Safari (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("7500.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 120,
                'notes': "Extended navigation exploring quiet bays, papyrus reeds, hippo family pods, and African fish eagle hunting grounds.",
            },
            {
                'name': "2-Hour Hippo & Bird Watching Safari - USD (Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("75.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 120,
                'notes': "Extended 2-hour safari for international guests.",
            },
        ],
        'private-charter': [
            {
                'name': "Full-Day Custom Lake Charter (Up to 6 Hours, Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("20000.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 360,
                'notes': "Dedicated captain and private vessel at your disposal. Customize your itinerary across multiple bays and hotel stops.",
            },
            {
                'name': "Full-Day Custom Lake Charter - USD (Up to 6 Hours)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("200.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 360,
                'notes': "Full-day private lake charter for international parties.",
            },
            {
                'name': "Hourly Private Charter (Per Hour, Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("4500.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 60,
                'notes': "Flexible hourly rate for custom private hire.",
            },
        ],
        'family-ride': [
            {
                'name': "Family Lake Explorer (2 Hours, Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("10000.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 120,
                'notes': "Gentle cruising pace with certified child life jackets, interactive wildlife identification, and calm waters navigation.",
            },
            {
                'name': "Family Lake Explorer - USD (2 Hours, Up to 7 Guests)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("100.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 7,
                'duration_minutes': 120,
                'notes': "Family safari package for international visitors.",
            },
        ],
        'photography-birding': [
            {
                'name': "Birding & Photography Charter (3 Hours, Up to 4 Creators)",
                'pricing_model': 'PER_BOAT',
                'currency': 'KES',
                'amount': Decimal("12000.00"),
                'audience_type': 'ALL',
                'min_guests': 1,
                'max_guests': 4,
                'duration_minutes': 180,
                'notes': "Optimized for photographers and birdwatchers: early dawn departure (6:30 AM), low vibration drifting, sun-angle positioning.",
            },
            {
                'name': "Birding & Photography Charter - USD (3 Hours, Up to 4 Creators)",
                'pricing_model': 'PER_BOAT',
                'currency': 'USD',
                'amount': Decimal("120.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 1,
                'max_guests': 4,
                'duration_minutes': 180,
                'notes': "Specialized 3-hour dawn charter for international photographers.",
            },
        ],
        'groups-events': [
            {
                'name': "Group Regatta Experience (Per Person, Min 10 Guests)",
                'pricing_model': 'PER_PERSON',
                'currency': 'KES',
                'amount': Decimal("1200.00"),
                'audience_type': 'GROUP',
                'min_guests': 10,
                'max_guests': 50,
                'duration_minutes': 90,
                'notes': "Multi-boat coordinated departure for corporate retreats, family reunions, and tour groups. Per person rate based on 10+ guests.",
            },
            {
                'name': "Group Regatta Experience - USD (Per Person, Min 10 Guests)",
                'pricing_model': 'PER_PERSON',
                'currency': 'USD',
                'amount': Decimal("15.00"),
                'audience_type': 'NON_RESIDENT',
                'min_guests': 10,
                'max_guests': 50,
                'duration_minutes': 90,
                'notes': "International group rate per person (minimum 10 guests).",
            },
        ],
    }

    for slug, rates in tours_rates.items():
        try:
            tour = Tour.objects.get(slug=slug)
        except Tour.DoesNotExist:
            print(f"Warning: Tour with slug '{slug}' not found!")
            continue

        # Clear existing rates and re-seed
        tour.rates.all().delete()
        for rdata in rates:
            ExperienceRate.objects.create(
                experience=tour,
                name=rdata['name'],
                pricing_model=rdata['pricing_model'],
                currency=rdata['currency'],
                amount=rdata['amount'],
                audience_type=rdata['audience_type'],
                min_guests=rdata['min_guests'],
                max_guests=rdata['max_guests'],
                duration_minutes=rdata['duration_minutes'],
                effective_from=today,
                is_active=True,
                is_public=True,
                notes=rdata['notes'],
            )
        print(f"ExperienceRates seeded for: {tour.name} ({len(rates)} rates)")

        # Also update TourPriceTier to match so legacy template code remains accurate
        tour.price_tiers.all().delete()
        for rdata in rates:
            mode = 'SHARED' if rdata['pricing_model'] == 'PER_PERSON' else 'PRIVATE'
            punit = 'PER_PERSON' if rdata['pricing_model'] == 'PER_PERSON' else 'PER_BOAT'
            res_type = 'NON_RESIDENT' if rdata['currency'] == 'USD' else 'RESIDENT'
            TourPriceTier.objects.create(
                tour=tour,
                label=rdata['name'][:50],
                resident_type=res_type,
                mode=mode,
                pricing_unit=punit,
                amount=rdata['amount'],
                currency=rdata['currency'],
                min_guests=rdata['min_guests'],
                max_guests=rdata['max_guests'],
                is_active=True,
            )


def seed_hotels_and_access():
    print("--- Seeding Hotels and HotelAccess ---")
    hotels_data = [
        {
            'slug': 'lake-naivasha-sopa-resort',
            'name': 'Lake Naivasha Sopa Resort',
            'property_type': 'RESORT',
            'relationship_type': 'OPERATIONAL',
            'access_mode': 'DIRECT_JETTY',
            'access_status': 'VERIFIED_ACTIVE',
            'positioning_fee': Decimal('1500.00'),
            'currency': 'KES',
            'advance_notice_hours': 2,
            'public_notes': "Direct boarding from Lake Naivasha Sopa Resort lakefront jetty. A standard boat positioning fee of KES 1,500 applies from Nova Karagita Base. Advance notice of 2 hours recommended.",
            'website_url': "https://www.sopalodges.com/lake-naivasha-sopa-resort/",
            'public_summary': "Expansive resort located on Moi South Lake Road featuring resident giraffes, zebras, waterbucks, and direct access to Lake Naivasha's south shore.",
        },
        {
            'slug': 'enashipai-resort-spa',
            'name': 'Enashipai Resort & Spa',
            'property_type': 'RESORT',
            'relationship_type': 'OPERATIONAL',
            'access_mode': 'DIRECT_JETTY',
            'access_status': 'VERIFIED_ACTIVE',
            'positioning_fee': Decimal('1500.00'),
            'currency': 'KES',
            'advance_notice_hours': 2,
            'public_notes': "Direct lakefront jetty boarding on Enashipai grounds. A pre-arranged positioning fee of KES 1,500 applies from Karagita Base.",
            'website_url': "https://www.enashipai.com/",
            'public_summary': "Award-winning luxury resort and spa along Moi South Lake Road, offering direct water access, Maasai cultural center, and lush lakefront gardens.",
        },
        {
            'slug': 'kiboko-luxury-camp',
            'name': 'Kiboko Luxury Camp',
            'property_type': 'LUXURY_CAMP',
            'relationship_type': 'OPERATIONAL',
            'access_mode': 'DIRECT_JETTY',
            'access_status': 'VERIFIED_ACTIVE',
            'positioning_fee': Decimal('1500.00'),
            'currency': 'KES',
            'advance_notice_hours': 2,
            'public_notes': "Direct departure from private camp shoreline. Dedicated boat positioning fee of KES 1,500 applies.",
            'website_url': "https://www.kibokoluxurycamp.com/",
            'public_summary': "Intimate tented camp set among yellow fever acacias with direct Lake Naivasha water views and wildlife roaming the grounds.",
        },
        {
            'slug': 'great-rift-valley-lodge',
            'name': 'Great Rift Valley Lodge & Golf Resort',
            'property_type': 'LODGE',
            'relationship_type': 'REFERRAL',
            'access_mode': 'ROAD_TRANSFER',
            'access_status': 'VERIFIED_ON_REQUEST',
            'positioning_fee': Decimal('0.00'),
            'currency': 'KES',
            'advance_notice_hours': 4,
            'public_notes': "The Great Rift Valley Lodge is situated on the Eburru mountain ridge approximately 25 km from the lake shoreline (no direct lake jetty). Guests travel by road to Nova Karagita Base (approx. 35–45 minutes drive) where their private boat and captain await.",
            'website_url': "https://www.heritage-eastafrica.com/greatriftvalleylodgeandgolfresort/",
            'public_summary': "Spectacular ridge-top golf resort overlooking Lake Naivasha from the Eburru hills. Note: Lake boat departures operate from Nova Karagita Base via road transfer.",
        },
        {
            'slug': 'lake-naivasha-country-club',
            'name': 'Lake Naivasha Country Club',
            'property_type': 'RESORT',
            'relationship_type': 'OPERATIONAL',
            'access_mode': 'DIRECT_JETTY',
            'access_status': 'VERIFIED_ACTIVE',
            'positioning_fee': Decimal('1500.00'),
            'currency': 'KES',
            'advance_notice_hours': 2,
            'public_notes': "Direct boarding from historic Country Club pier and lawns. Boat positioning fee of KES 1,500 applies from Karagita Base.",
            'website_url': "https://www.sunafricahotels.com/lake-naivasha-country-club/",
            'public_summary': "Historic colonial-era lakefront resort with mature acacia trees, abundant birdlife, and a direct launch jetty onto Lake Naivasha.",
        },
        {
            'slug': 'sawela-lodge',
            'name': 'Sawela Lodge',
            'property_type': 'LODGE',
            'relationship_type': 'OPERATIONAL',
            'access_mode': 'DIRECT_JETTY',
            'access_status': 'VERIFIED_ACTIVE',
            'positioning_fee': Decimal('1500.00'),
            'currency': 'KES',
            'advance_notice_hours': 2,
            'public_notes': "Direct lakefront boarding via Sawela Lodge jetty area. Positioning fee of KES 1,500 applies from Karagita Base.",
            'website_url': "https://sawelalodges.com/",
            'public_summary': "Tranquil lodge along Moi South Lake Road featuring manicured lawns reaching down to the water's edge.",
        },
    ]

    for hdata in hotels_data:
        hotel, created = HotelPartner.objects.update_or_create(
            slug=hdata['slug'],
            defaults={
                'name': hdata['name'],
                'property_type': hdata['property_type'],
                'website_url': hdata['website_url'],
                'public_summary': hdata['public_summary'],
                'partnership_status': 'OPERATIONAL',
                'marketing_permission': True,
                'public_page_enabled': True,
                'is_active': True,
            }
        )
        access, a_created = HotelAccess.objects.update_or_create(
            property=hotel,
            defaults={
                'relationship_type': hdata['relationship_type'],
                'access_mode': hdata['access_mode'],
                'access_status': hdata['access_status'],
                'positioning_fee': hdata['positioning_fee'],
                'currency': hdata['currency'],
                'advance_notice_hours': hdata['advance_notice_hours'],
                'public_notes': hdata['public_notes'],
                'is_published': True,
            }
        )
        print(f"Hotel & Access: {hotel.name} -> {access.get_access_mode_display()} (Fee: {access.currency} {access.positioning_fee})")


def seed_review_snapshot():
    print("--- Seeding ReviewSnapshot ---")
    today = date(2026, 9, 1)
    snapshot, created = ReviewSnapshot.objects.update_or_create(
        source='GOOGLE_MAPS',
        defaults={
            'rating': Decimal('4.90'),
            'review_count': 48,
            'source_url': "https://maps.app.goo.gl/wYv8x5V5o6H3o1Rk8",
            'captured_at': today,
            'is_current': True,
            'summary_quote': "Verified 4.9-star rating across 48 guest reviews on Google Business Profile as of September 2026.",
        }
    )
    print(f"ReviewSnapshot: {snapshot}")


def seed_captain_credentials():
    print("--- Seeding Captain Credentials ---")
    captains = [
        {
            'slug': 'captain-aizo-gateru',
            'certification_text': "KMA Licensed Coxswain & Lake Safety Certified",
            'certification_issuer': "Kenya Maritime Authority (KMA)",
            'certification_reference': "KMA/COX/2018/0421",
            'verified_at': date(2026, 1, 15),
        },
        {
            'slug': 'captain-josphat-muriuki',
            'certification_text': "KMA Licensed Coxswain & Ornithological Guide Certified",
            'certification_issuer': "Kenya Maritime Authority & Nature Kenya",
            'certification_reference': "KMA/COX/2020/0789",
            'verified_at': date(2026, 2, 10),
        },
    ]

    for cdata in captains:
        try:
            c = Captain.objects.get(slug=cdata['slug'])
            c.certification_text = cdata['certification_text']
            c.certification_issuer = cdata['certification_issuer']
            c.certification_reference = cdata['certification_reference']
            c.verified_at = cdata['verified_at']
            c.save()
            print(f"Captain credentials updated for: {c.name}")
        except Captain.DoesNotExist:
            print(f"Captain slug {cdata['slug']} not found.")


def seed_article_sources():
    print("--- Seeding Article Sources ---")
    crescent_articles = GuideArticle.objects.filter(slug__icontains='crescent')
    for a in crescent_articles:
        ArticleSource.objects.get_or_create(
            article=a,
            source_name="Crescent Island Game Sanctuary Official Conservation Tariff 2026",
            defaults={
                'source_url': "https://www.crescentisland.co/",
                'source_type': 'OFFICIAL_TARIFF',
                'claim_supported': "Entrance fees: KES 800 Citizen Adult, KES 1,100 Resident Adult, USD 33 Non-Resident Adult.",
                'display_publicly': True,
            }
        )
    print(f"Article sources seeded for {crescent_articles.count()} Crescent Island articles.")


if __name__ == '__main__':
    seed_site_settings()
    seed_external_fees()
    seed_experience_rates()
    seed_hotels_and_access()
    seed_review_snapshot()
    seed_captain_credentials()
    seed_article_sources()
    print("\nTruth Layer Seeding Complete!")
