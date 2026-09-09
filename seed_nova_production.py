import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import SiteSettings
from tours.models import Tour, TourPriceTier, AddOn
from partners.models import HotelPartner, HotelServicePoint, HotelTourService
from stays.models import AccommodationProperty, RoomType, AccommodationRate
from packages.models import Package, PackageComponent
from content.models import Captain, GuideArticle, QuestionAnswer, Testimonial

print("=== SEEDING NOVA BOAT RIDES NAIVASHA PRODUCTION DATA ===")

# 1. SITE SETTINGS
settings, created = SiteSettings.objects.get_or_create(pk=1)
settings.business_name = "Nova Boat Rides Naivasha"
settings.legal_name = "Nova Boat Rides Naivasha Ltd"
settings.tagline = "Naivasha starts here."
settings.supporting_proposition = "Boat rides, hotel departures and curated stays around Lake Naivasha — planned through one local team."
settings.phone_display = "+254 700 000 000"
settings.phone_e164 = "+254700000000"
settings.whatsapp_number = "254700000000"
settings.email = "hello@novaboatrider.com"
settings.standard_launch_name = "Nova Lake Base, South Lake Road, Naivasha"
settings.standard_launch_lat = Decimal('-0.757200')
settings.standard_launch_lng = Decimal('36.354200')
settings.operating_hours = "Daily 6:30 AM – 6:30 PM"
settings.default_currency = "KES"
settings.directions_summary = "Located off South Lake Road, Naivasha. Private parking, dedicated briefing jetty, life jacket fitting station, and guest lounge on site."
settings.booking_notice = "Advance booking recommended for hotel departures, Crescent Island walks, and sunset charters."
settings.save()
print("[OK] SiteSettings configured.")

# 2. TOURS & TIERS
tours_data = [
    {
        'name': 'Classic Lake Safari',
        'slug': 'classic-lake-safari',
        'summary': 'The essential Lake Naivasha introduction: hippo pools, fish eagle habitats, and flooded forest routes with a certified captain.',
        'body': 'Experience the open waters of Lake Naivasha at a relaxed pace. Your certified Nova captain guides you along acacia-fringed shorelines where resident hippo pods rest in shallows. Watch African fish eagles dive with remarkable accuracy and spot pelicans, cormorants, and herons.',
        'duration_hours': Decimal('1.0'),
        'capacity': 8,
        'is_private': False,
        'is_shared': True,
        'standard_departure': 'Nova Lake Base or Approved Hotel Jetty',
        'best_for': 'First-time visitors, day-trippers, couples, families',
        'route_narrative': 'Departing Nova Lake Base heading eastward across Karagita bay toward the central papyrus lagoons and hippo pools.',
        'what_guests_may_see': 'Resident hippo pods, African fish eagles, pied kingfishers, yellow-billed storks, black cormorants, and giraffe on shorelines.',
        'order': 1,
        'is_featured': True,
        'tiers': [
            {'label': 'Resident Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 3000, 'curr': 'KES'},
            {'label': 'International Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'NON_RESIDENT', 'unit': 'PER_PERSON', 'amount': 25, 'curr': 'USD'},
            {'label': 'Private Charter (up to 7)', 'min': 1, 'max': 7, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 16000, 'curr': 'KES'},
        ]
    },
    {
        'name': 'Hippo & Bird Safari',
        'slug': 'hippo-bird-safari',
        'summary': 'Extended wildlife voyage exploring secluded lagoons, papyrus channels, and active water bird hunting grounds.',
        'body': 'A deeper wildlife exploration designed for wildlife enthusiasts and photographers. Navigating quieter water channels away from busy launch corridors, this 90-minute cruise allows quiet drifting near pods of hippos and prime perches of goliath herons, kingfishers, and osprey.',
        'duration_hours': Decimal('1.5'),
        'capacity': 8,
        'is_private': False,
        'is_shared': True,
        'standard_departure': 'Nova Lake Base or Approved Hotel Jetty',
        'best_for': 'Wildlife enthusiasts, bird watchers, small groups',
        'route_narrative': 'Circumnavigating southern papyrus reed beds, deep water channels, and sheltered coves with optimal morning light.',
        'what_guests_may_see': 'Over 40 recorded bird species, hippo families with juveniles, waterbuck grazing near lake edges.',
        'order': 2,
        'is_featured': True,
        'tiers': [
            {'label': 'Resident Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 4500, 'curr': 'KES'},
            {'label': 'International Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'NON_RESIDENT', 'unit': 'PER_PERSON', 'amount': 35, 'curr': 'USD'},
            {'label': 'Private Charter (up to 7)', 'min': 1, 'max': 7, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 22000, 'curr': 'KES'},
        ]
    },
    {
        'name': 'Crescent Island Boat Transfer & Walking Tour',
        'slug': 'crescent-island',
        'summary': 'Combine scenic lake boat transit with a guided walking safari among wild giraffe, zebra, wildebeest, and gazelle on Crescent Island.',
        'body': 'Cross the open lake by boat to Crescent Island Game Sanctuary, one of the few places in East Africa where visitors walk freely among wild herbivores without predator danger. Walk among towers of giraffe, zebra herds, wildebeest, and waterbuck.',
        'duration_hours': Decimal('2.0'),
        'capacity': 8,
        'is_private': False,
        'is_shared': True,
        'standard_departure': 'Nova Lake Base or Approved Hotel Jetty',
        'best_for': 'Families, couples, international safari travelers',
        'route_narrative': 'Open lake crossing directly to the private western jetty of Crescent Island, followed by a guided walking circuit.',
        'what_guests_may_see': 'Giraffe, Burchell zebra, blue wildebeest, Thomson gazelle, impala, dik-dik, hippos basking.',
        'order': 3,
        'is_featured': True,
        'tiers': [
            {'label': 'Resident Boat Transit', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 5500, 'curr': 'KES'},
            {'label': 'International Boat Transit', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'NON_RESIDENT', 'unit': 'PER_PERSON', 'amount': 45, 'curr': 'USD'},
            {'label': 'Private Return Charter', 'min': 1, 'max': 7, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 25000, 'curr': 'KES'},
        ]
    },
    {
        'name': 'Sunset Lake Cruise',
        'slug': 'sunset-cruise',
        'summary': 'Golden hour over the Great Rift Valley escarpment. Glass-calm water, silhouettes of drowned trees, and evening hippo movement.',
        'body': 'As the equatorial sun drops behind the Mau Escarpment, Lake Naivasha turns into liquid gold. Hippos begin active movement toward night feeding grounds, fish eagles call from roosts, and the water mirrors pink and violet sky tones.',
        'duration_hours': Decimal('1.5'),
        'capacity': 8,
        'is_private': False,
        'is_shared': True,
        'standard_departure': 'Nova Lake Base or Approved Hotel Jetty',
        'best_for': 'Couples, anniversaries, photographers, relaxation',
        'route_narrative': 'Departing 17:00 toward western open waters, positioning for panoramic sunset alignment across the Rift Valley crater rims.',
        'what_guests_may_see': 'Dramatic Rift Valley sunsets, active hippo herds entering shallow grasslands, night heron emergence.',
        'order': 4,
        'is_featured': True,
        'tiers': [
            {'label': 'Resident Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 5000, 'curr': 'KES'},
            {'label': 'International Adult', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'NON_RESIDENT', 'unit': 'PER_PERSON', 'amount': 40, 'curr': 'USD'},
            {'label': 'Private Sunset Charter', 'min': 1, 'max': 7, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 24000, 'curr': 'KES'},
        ]
    },
    {
        'name': 'Private Lake Charter',
        'slug': 'private-charter',
        'summary': 'Exclusive boat, dedicated senior captain, flexible timing, and custom route tailored entirely to your party.',
        'body': 'Complete privacy and scheduling flexibility on Lake Naivasha. Depart when you wish, focus on your specific interests—whether wildlife photography, family leisure, or celebration—and choose your boarding point from approved partner jetties.',
        'duration_hours': Decimal('2.0'),
        'capacity': 8,
        'is_private': True,
        'is_shared': False,
        'standard_departure': 'Guest Choice: Hotel Jetty or Nova Lake Base',
        'best_for': 'Celebrations, VIP guests, private families, creator crews',
        'route_narrative': 'Custom itinerary designed with your senior captain before casting off.',
        'what_guests_may_see': 'Tailored according to selected route and time of day.',
        'order': 5,
        'is_featured': False,
        'tiers': [
            {'label': 'Private Charter (2 Hours)', 'min': 1, 'max': 8, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 28000, 'curr': 'KES'},
            {'label': 'International Charter', 'min': 1, 'max': 8, 'mode': 'PRIVATE', 'res': 'NON_RESIDENT', 'unit': 'PER_BOAT', 'amount': 220, 'curr': 'USD'},
        ]
    },
    {
        'name': 'Family Lake Explorer',
        'slug': 'family-ride',
        'summary': 'Calm water routes, child-fitted safety gear, engaging nature storytelling, and guaranteed gentle handling.',
        'body': 'Designed from the ground up for families with young children or elders. Short, gentle boarding paths, specially certified child life jackets, and a captain who shares fascinating facts about hippo communication and bird nesting.',
        'duration_hours': Decimal('1.2'),
        'capacity': 8,
        'is_private': False,
        'is_shared': True,
        'standard_departure': 'Nova Lake Base or Approved Hotel Jetty',
        'best_for': 'Families with children, multi-generational groups',
        'route_narrative': 'Protected shoreline bays with minimal wave action and constant wildlife visibility.',
        'what_guests_may_see': 'Baby hippos, swimming cormorants, lily pad ecosystems, water monitors.',
        'order': 6,
        'is_featured': False,
        'tiers': [
            {'label': 'Family Ticket (2 Adults + 2 Kids)', 'min': 1, 'max': 4, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 10000, 'curr': 'KES'},
            {'label': 'Additional Guest', 'min': 1, 'max': 8, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 2500, 'curr': 'KES'},
        ]
    },
    {
        'name': 'Birding & Creative Photography Charter',
        'slug': 'photography-birding',
        'summary': 'Early morning calm water positioning, silence protocols, tripod space, and light alignment for birders and filmmakers.',
        'body': 'Lake Naivasha is a Ramsar wetland of international importance with over 400 bird species. This early morning departure gives serious photographers and birders low-angle light, motor-cut silent drifting, and specialized positioning.',
        'duration_hours': Decimal('2.5'),
        'capacity': 6,
        'is_private': True,
        'is_shared': False,
        'standard_departure': 'Nova Lake Base (06:30 AM recommended)',
        'best_for': 'Avid birders, telephoto photographers, documentary crews',
        'route_narrative': 'Eastern wetlands, flooded acacia zones, and Oloidien bay channels during sunrise golden hour.',
        'what_guests_may_see': 'Goliath heron, African skimmer, malachite kingfisher, African jacana, saddle-billed stork.',
        'order': 7,
        'is_featured': False,
        'tiers': [
            {'label': 'Specialist Charter (Up to 5)', 'min': 1, 'max': 5, 'mode': 'PRIVATE', 'res': 'RESIDENT', 'unit': 'PER_BOAT', 'amount': 32000, 'curr': 'KES'},
            {'label': 'International Charter', 'min': 1, 'max': 5, 'mode': 'PRIVATE', 'res': 'NON_RESIDENT', 'unit': 'PER_BOAT', 'amount': 250, 'curr': 'USD'},
        ]
    },
    {
        'name': 'Corporate & Group Lake Regatta',
        'slug': 'groups-events',
        'summary': 'Multi-boat coordination, passenger manifests, hotel conference pickups, and structured lake rallies for teams.',
        'body': 'Nova coordinates corporate lake days and conference breaks with precision. Synchronized fleet departures, safety manifests, team challenges, and direct pickup from conference resort jetties.',
        'duration_hours': Decimal('2.0'),
        'capacity': 30,
        'is_private': True,
        'is_shared': False,
        'standard_departure': 'Partner Resort Jetty or Nova Lake Base',
        'best_for': 'Corporate retreats, conference breakouts, school trips, weddings',
        'route_narrative': 'Multi-boat coordinated cruise with lake rally waypoints.',
        'what_guests_may_see': 'Expansive lake vistas, wildlife pods, collaborative flotilla.',
        'order': 8,
        'is_featured': False,
        'tiers': [
            {'label': 'Group Tier (Per Person KES)', 'min': 10, 'max': 50, 'mode': 'SHARED', 'res': 'RESIDENT', 'unit': 'PER_PERSON', 'amount': 3000, 'curr': 'KES'},
        ]
    }
]

for tdata in tours_data:
    tiers = tdata.pop('tiers')
    tour, _ = Tour.objects.update_or_create(slug=tdata['slug'], defaults=tdata)
    tour.price_tiers.all().delete()
    for tier_data in tiers:
        TourPriceTier.objects.create(
            tour=tour,
            label=tier_data['label'],
            min_guests=tier_data['min'],
            max_guests=tier_data['max'],
            mode=tier_data['mode'],
            resident_type=tier_data['res'],
            pricing_unit=tier_data['unit'],
            amount=Decimal(str(tier_data['amount'])),
            currency=tier_data['curr'],
            is_active=True
        )
print(f"[OK] Seeded {len(tours_data)} Tours with tiered pricing.")

# 3. ADD-ONS
addons_data = [
    {'name': 'Crescent Island Sanctuary Guide', 'slug': 'crescent-guide', 'price_mode': 'FLAT', 'amount': 1500, 'description': 'Dedicated sanctuary ranger guide during your Crescent Island walking safari.'},
    {'name': 'Sunset Sparkling Wine & Fruit Basket', 'slug': 'sunset-wine-basket', 'price_mode': 'FLAT', 'amount': 3500, 'description': 'Chilled sparkling wine, fresh Naivasha strawberries, and artisanal cheese board for sunset cruises.'},
    {'name': 'Spotting Scope & Bird Checklist', 'slug': 'birding-kit', 'price_mode': 'FLAT', 'amount': 2000, 'description': 'Professional tripod-mounted spotting scope and laminated Lake Naivasha bird species checklist.'},
]
for adata in addons_data:
    AddOn.objects.update_or_create(slug=adata['slug'], defaults=adata)
print(f"[OK] Seeded {len(addons_data)} Add-ons.")

# 4. HOTEL PARTNERS & SERVICE POINTS
partners_data = [
    {
        'name': 'Lake Naivasha Sopa Resort',
        'slug': 'lake-naivasha-sopa-resort',
        'property_type': 'RESORT',
        'public_summary': 'Expansive 150-acre lakeside property along South Lake Road with resident giraffe and waterbuck roaming open lawns.',
        'website_url': 'https://www.lakenaivasha-soparesort.com/',
        'partnership_status': 'PROSPECT',
        'marketing_permission': False,
        'public_page_enabled': False,  # Sopa rule: disabled by default until verified agreement!
        'service_points': [
            {
                'name': 'Sopa Lakefront Jetty',
                'service_mode': 'PARTNER_JETTY',
                'public_instructions': 'Meet your captain at the Sopa private wooden jetty at the lower lawn edge 10 minutes prior to scheduled departure.',
                'private_ops_notes': 'Shallow water approach during low lake levels; captain must verify depth clearance 2 hours prior.',
                'operating_window': '07:00 – 17:30',
                'notice_hours': 24,
                'positioning_fee': Decimal('2000.00'),
            },
            {
                'name': 'Sopa Gate Shuttle Pickup',
                'service_mode': 'PARTNER_TRANSFER',
                'public_instructions': 'Nova transfer vehicle meets guests at Sopa main reception lobby for the 10-minute drive to Nova Lake Base.',
                'private_ops_notes': 'Standard vehicle transfer via South Lake Road.',
                'operating_window': '06:30 – 18:00',
                'notice_hours': 4,
                'positioning_fee': Decimal('1000.00'),
            }
        ]
    },
    {
        'name': 'Enashipai Resort & Spa',
        'slug': 'enashipai-resort-spa',
        'property_type': 'RESORT',
        'public_summary': 'Upscale resort on South Lake Road with extensive conference facilities, lake access, and Sasaab Maasai museum.',
        'website_url': 'https://www.enashipai.com/',
        'partnership_status': 'VERIFIED',
        'marketing_permission': True,
        'public_page_enabled': True,
        'service_points': [
            {
                'name': 'Enashipai Gate Transfer',
                'service_mode': 'PARTNER_TRANSFER',
                'public_instructions': 'Nova transfer vehicle meets guests at Enashipai main porte-cochere for the 8-minute transfer to Nova Lake Base.',
                'private_ops_notes': 'Vehicle entry pass pre-cleared at security gate.',
                'operating_window': '06:30 – 18:00',
                'notice_hours': 3,
                'positioning_fee': Decimal('1000.00'),
            }
        ]
    },
    {
        'name': 'Kiboko Luxury Camp',
        'slug': 'kiboko-luxury-camp',
        'property_type': 'CAMP',
        'public_summary': 'Intimate tented luxury camp nestled under yellow-barked acacia trees directly on the water shoreline.',
        'website_url': 'https://kibokocamps.com/',
        'partnership_status': 'VERIFIED',
        'marketing_permission': True,
        'public_page_enabled': True,
        'service_points': [
            {
                'name': 'Kiboko Direct Boardwalk Jetty',
                'service_mode': 'PARTNER_JETTY',
                'public_instructions': 'Walk down the camp timber boardwalk directly to the boat mooring pontoon.',
                'private_ops_notes': 'Excellent deep water mooring point year round.',
                'operating_window': '06:30 – 17:30',
                'notice_hours': 6,
                'positioning_fee': Decimal('1500.00'),
            }
        ]
    },
    {
        'name': 'Great Rift Valley Lodge',
        'slug': 'great-rift-valley-lodge',
        'property_type': 'LODGE',
        'public_summary': 'Panoramic lodge perched 7,000 feet above Lake Naivasha on the Eburru ridge with championship golf and escarpment views.',
        'website_url': 'https://www.heritage-eastafrica.com/great-rift-valley-lodge-and-golf-resort/',
        'partnership_status': 'VERIFIED',
        'marketing_permission': True,
        'public_page_enabled': True,
        'service_points': [
            {
                'name': 'Ridge to Lake Vehicle Transfer',
                'service_mode': 'PARTNER_TRANSFER',
                'public_instructions': 'Nova private safari van picks guests up from lodge reception for the scenic 35-minute descent to Nova Lake Base.',
                'private_ops_notes': 'Allow 40 minutes road travel time due to mountain road bends.',
                'operating_window': '07:00 – 16:30',
                'notice_hours': 12,
                'positioning_fee': Decimal('3000.00'),
            }
        ]
    }
]

for pdata in partners_data:
    sp_data_list = pdata.pop('service_points')
    partner, _ = HotelPartner.objects.update_or_create(slug=pdata['slug'], defaults=pdata)
    for sp_data in sp_data_list:
        pos_fee = sp_data.pop('positioning_fee')
        sp, _ = HotelServicePoint.objects.update_or_create(hotel=partner, name=sp_data['name'], defaults=sp_data)
        # Link all active tours
        for tour in Tour.objects.filter(is_active=True):
            HotelTourService.objects.update_or_create(
                service_point=sp,
                tour=tour,
                defaults={
                    'service_mode': sp.service_mode,
                    'positioning_fee': pos_fee,
                    'requires_manual_confirmation': True,
                    'is_active': True
                }
            )
print(f"[OK] Seeded {len(partners_data)} Hotel Partners and Service Points.")

# 5. ACCOMMODATION PROPERTIES & RATES
stays_data = [
    {
        'name': 'Lake Naivasha Sopa Resort',
        'slug': 'lake-naivasha-sopa-resort',
        'inventory_mode': 'ENQUIRY',
        'property_type': 'RESORT',
        'summary': 'Sprawling 150-acre lakeside resort with direct water frontage, resident wildlife on lawns, and large cottage suites.',
        'why_nova_recommends': 'Resident giraffe graze steps from guest balconies, and Nova can coordinate direct jetty departures when water levels permit.',
        'amenities': 'Swimming Pool, Waterfront Gardens, Safari Bar, 2 Restaurants, Fitness Center, Tennis Courts',
        'starting_price': Decimal('26000.00'),
        'currency': 'KES',
        'price_basis': 'per cottage room / night (Full Board)',
        'order': 1,
        'is_featured': True,
    },
    {
        'name': 'Enashipai Resort & Spa',
        'slug': 'enashipai-resort-spa',
        'inventory_mode': 'ENQUIRY',
        'property_type': 'RESORT',
        'summary': 'Award-winning lakeside luxury resort known for modern rooms, Entumo conference center, and the Maa Spa.',
        'why_nova_recommends': 'Central South Lake location makes transfers to Nova launch base effortless; ideal for couples and conference attendees.',
        'amenities': 'Luxury Spa, Heated Pool, Fine Dining, Sasaab Museum, Fitness Centre, Children Play Zone',
        'starting_price': Decimal('32000.00'),
        'currency': 'KES',
        'price_basis': 'per executive room / night (Bed & Breakfast)',
        'order': 2,
        'is_featured': True,
    },
    {
        'name': 'Kiboko Luxury Camp',
        'slug': 'kiboko-luxury-camp',
        'inventory_mode': 'ALLOTMENT',
        'property_type': 'CAMP',
        'summary': 'Exclusive 8-tent boutique safari camp situated directly on the shoreline under dense acacia forest.',
        'why_nova_recommends': 'The most intimate water experience on Lake Naivasha. Private boardwalk jetty boarding for sunset cruises and early morning birding.',
        'amenities': 'Waterfront Dining Deck, Private Butler Service, Campfire Boma, Solar Power, Wi-Fi',
        'starting_price': Decimal('48000.00'),
        'currency': 'KES',
        'price_basis': 'per luxury tent / night (All-Inclusive)',
        'order': 3,
        'is_featured': True,
    },
    {
        'name': 'Camp Carnelley\'s Bandas & Cottages',
        'slug': 'camp-carnelleys-cottages',
        'inventory_mode': 'MANAGED',
        'property_type': 'COTTAGES',
        'summary': 'Bohemian lakeside cottages and bandas nestled under mature yellow-fever acacias with the beloved Lazybones bar.',
        'why_nova_recommends': 'Relaxed, creative lake vibe with direct water access. Great value for young couples, artists, and active weekenders.',
        'amenities': 'Lazybones Bar & Restaurant, Campfire Pit, Lakeside Hammocks, Hot Showers, Wi-Fi',
        'starting_price': Decimal('14000.00'),
        'currency': 'KES',
        'price_basis': 'per banda / night (Room Only)',
        'order': 4,
        'is_featured': False,
    }
]

for sdata in stays_data:
    partner = HotelPartner.objects.filter(slug=sdata['slug']).first()
    prop, _ = AccommodationProperty.objects.update_or_create(
        slug=sdata['slug'],
        defaults={
            **sdata,
            'partner': partner,
            'description': sdata['summary'] + ' ' + sdata['why_nova_recommends']
        }
    )
    # Create sample room type
    rt, _ = RoomType.objects.update_or_create(
        property=prop,
        name='Standard Double Suite',
        defaults={'max_adults': 2, 'max_children': 1, 'bed_configuration': '1 King Bed'}
    )
    AccommodationRate.objects.update_or_create(
        room_type=rt,
        meal_plan='BB',
        resident_type='RESIDENT',
        defaults={'amount': sdata['starting_price'], 'currency': sdata['currency'], 'is_available': True}
    )
print(f"[OK] Seeded {len(stays_data)} Accommodation Properties with Rates.")

# 6. PACKAGES
packages_data = [
    {
        'name': 'Stay + Ride Weekend Escape',
        'slug': 'stay-and-ride',
        'tagline': 'Lakeside Accommodation + Morning Wildlife Safari',
        'summary': 'Check into a verified lakefront lodge, enjoy dinner by the water, and wake up to a private boat departure directly from your hotel jetty or base.',
        'description': 'The quintessential Lake Naivasha weekend. Combines one night of curated accommodation with a 90-minute Hippo & Bird Safari and hotel-origin pickup coordination.',
        'duration_days': 2,
        'duration_nights': 1,
        'starting_price': Decimal('36000.00'),
        'currency': 'KES',
        'price_basis': 'per couple / 1 night stay + safari boat ride',
        'includes_hotel_origin_pickup': True,
        'includes_crescent_island': False,
        'order': 1,
        'is_featured': True,
        'components': [
            ('Lakeside Check-in', 'HOTEL', 'Check in at selected partner property from 14:00. Relax on open lawns watching wildlife.'),
            ('Sunset Relaxation', 'MEAL', 'Evening dinner by the water under yellow-fever acacias.'),
            ('Hotel Departure', 'TRANSFER', 'Captain positions boat to your hotel jetty or Nova transfer vehicle arrives at 08:30.'),
            ('Morning Hippo & Bird Safari', 'BOAT', '90-minute guided wildlife cruise spotting hippos, fish eagles, and kingfishers.'),
        ]
    },
    {
        'name': 'Couples Romantic Lake Escape',
        'slug': 'couples-lake-escape',
        'tagline': 'Luxury Tent Stay + Private Sunset Champagne Cruise',
        'summary': 'Intimate getaway featuring luxury tented accommodation, sparkling wine, and a private golden hour sunset cruise on Lake Naivasha.',
        'description': 'Designed for proposals, anniversaries, and romantic weekends. Includes private return charter, champagne basket, and luxury tented accommodation with lakefront deck.',
        'duration_days': 2,
        'duration_nights': 1,
        'starting_price': Decimal('54000.00'),
        'currency': 'KES',
        'price_basis': 'per couple / luxury tent + private sunset charter',
        'includes_hotel_origin_pickup': True,
        'includes_crescent_island': False,
        'order': 2,
        'is_featured': True,
        'components': [
            ('Check-in & Welcome Drinks', 'HOTEL', 'Private arrival at luxury boutique tented camp.'),
            ('Private Sunset Charter', 'BOAT', 'Exclusive boat departure at 17:00 with chilled sparkling wine and fruit basket.'),
            ('Rift Valley Starlight Dinner', 'MEAL', 'Three-course fireside dinner under the African night sky.'),
        ]
    },
    {
        'name': 'Family Naivasha Weekend',
        'slug': 'family-naivasha-weekend',
        'tagline': 'Family Cottage + Crescent Island Walking Safari',
        'summary': 'Spacious family cottage stay, gentle lake cruise, and walking among wild giraffe and zebra on Crescent Island.',
        'description': 'A hassle-free 3-day family itinerary planned with child safety and gentle water routes in mind. Includes family suite, boat transit, and guided walking tour.',
        'duration_days': 3,
        'duration_nights': 2,
        'starting_price': Decimal('72000.00'),
        'currency': 'KES',
        'price_basis': 'for family of 4 (2 adults, 2 kids) / 2 nights + Crescent Island',
        'includes_hotel_origin_pickup': True,
        'includes_crescent_island': True,
        'order': 3,
        'is_featured': True,
        'components': [
            ('Family Cottage Arrival', 'HOTEL', 'Spacious cottage check-in with private lawn for kids to play safely.'),
            ('Gentle Morning Lake Cruise', 'BOAT', 'Child-fitted life jackets and educational storytelling on the water.'),
            ('Crescent Island Walking Safari', 'ACTIVITY', 'Walk among wild giraffe, zebra, and gazelle with a certified guide.'),
        ]
    },
    {
        'name': 'Hell\'s Gate + Lake Combo Day',
        'slug': 'hells-gate-and-lake',
        'tagline': 'Gorge Hike & Cycling + Sunset Boat Safari',
        'summary': 'The ultimate active Naivasha day: cycle through Hell\'s Gate National Park in the morning, followed by an afternoon wildlife boat safari.',
        'description': 'Full day of Rift Valley adventure. Morning bicycle ride through dramatic volcanic towers in Hell\'s Gate, gorge hike, followed by fresh lakeside lunch and relaxing sunset boat safari.',
        'duration_days': 1,
        'duration_nights': 0,
        'starting_price': Decimal('12500.00'),
        'currency': 'KES',
        'price_basis': 'per person (includes bike hire, park escort, boat ride)',
        'includes_hotel_origin_pickup': False,
        'includes_crescent_island': False,
        'order': 4,
        'is_featured': False,
        'components': [
            ('Hell\'s Gate Cycling & Gorge', 'ACTIVITY', 'Morning bicycle safari past Fischer\'s Tower and guided gorge walk.'),
            ('Lakeside Lunch', 'MEAL', 'Relaxed fresh lunch by the water at Nova Lake Base.'),
            ('Afternoon Boat Safari', 'BOAT', '90-minute wildlife cruise to unwind after your morning hike.'),
        ]
    }
]

for pdata in packages_data:
    components = pdata.pop('components')
    pkg, _ = Package.objects.update_or_create(slug=pdata['slug'], defaults=pdata)
    pkg.eligible_tours.set(Tour.objects.filter(is_active=True)[:2])
    pkg.accommodation_properties.set(AccommodationProperty.objects.filter(is_active=True)[:2])
    pkg.components.all().delete()
    for i, (title, ctype, desc) in enumerate(components):
        PackageComponent.objects.create(
            package=pkg,
            title=title,
            component_type=ctype,
            description=desc,
            order=i
        )
print(f"[OK] Seeded {len(packages_data)} Packages.")

# 7. CAPTAINS & CREW
Captain.objects.update_or_create(
    slug='captain-dennis-maina',
    defaults={
        'name': 'Captain Dennis Maina',
        'role_title': 'Senior Lake Operations Lead & Captain',
        'years_on_lake': 12,
        'route_specialties': 'Hippo family territories, Crescent Island navigation, late afternoon wind management',
        'languages': 'English, Swahili',
        'bio': 'Dennis has navigated Lake Naivasha daily for over a decade. His intimate knowledge of changing water levels and hippo pod movements ensures guests experience the lake safely and at the most rewarding times.',
        'quote': 'The lake changes every single week. Knowing where the water is deep, where the hippos feed, and when the wind will rise is what makes a great lake day.',
        'order': 1,
        'is_active': True,
    }
)
print("[OK] Seeded Captain profiles.")

# 8. TESTIMONIALS
testimonials_data = [
    {
        'guest_name': 'Wanjiku & Brian M.',
        'guest_segment': 'COUPLE',
        'rating': 5,
        'text': 'We booked the Sunset Cruise from Sopa. Having the boat arrive at the hotel jetty made our anniversary completely effortless. Dennis was a phenomenal captain!',
        'trip_date': 'August 2026',
        'is_featured': True,
    },
    {
        'guest_name': 'Markus & Elena Schneider',
        'guest_segment': 'HOTEL_GUEST',
        'rating': 5,
        'text': 'The most organized experience of our 2-week Kenya safari. Clear pricing upfront, spotless boat, proper life vests for our kids, and incredible views of the fish eagles.',
        'trip_date': 'July 2026',
        'is_featured': True,
    },
    {
        'guest_name': 'Pooja K. & Family',
        'guest_segment': 'FAMILY',
        'rating': 5,
        'text': 'Crescent Island by boat was magical. Walking five meters away from wild giraffes with no barriers was unforgettable. Nova made the logistics seamless.',
        'trip_date': 'August 2026',
        'is_featured': True,
    },
    {
        'guest_name': 'David T. (Nairobi Day-Tripper)',
        'guest_segment': 'GROUP',
        'rating': 5,
        'text': 'Left Nairobi at 7:00 AM, had our boat in Naivasha by 9:30 AM, and enjoyed a fantastic Hell\'s Gate combo. Instant WhatsApp response and total price transparency.',
        'trip_date': 'September 2026',
        'is_featured': True,
    }
]
for tdata in testimonials_data:
    Testimonial.objects.update_or_create(guest_name=tdata['guest_name'], defaults=tdata)
print(f"[OK] Seeded {len(testimonials_data)} Testimonials.")

# 9. QUESTIONS & ANSWERS (8 BOOKING BLOCKERS §10)
faqs_data = [
    {
        'question': 'Can Nova pick me up or depart directly from my hotel?',
        'category': 'HOTEL_PICKUP',
        'plain_answer': 'Yes. Nova coordinates direct jetty departures from verified lakefront hotels where water depth allows, or arranges seamless private road pickup to our central launch base.',
        'answer': '<p>Yes. If you are staying at an approved partner hotel with a functional jetty (such as Sopa or Kiboko), we can position a boat to board you directly from your hotel lawn. For properties set back from the water or without active jetties, we provide vehicle pickup to Nova Lake Base.</p>',
        'order': 1,
        'is_featured': True
    },
    {
        'question': 'How much does a Lake Naivasha boat ride cost?',
        'category': 'PRICES',
        'plain_answer': 'Standard shared safaris start from KES 3,000 ($25) per adult. Private charters start from KES 16,000 ($130) per boat for up to 7 passengers.',
        'answer': '<p>Our transparent pricing is published by duration and group size. A 1-hour Classic Safari starts at KES 3,000 per resident adult ($25 international). Private boat charters start at KES 16,000 per boat for the complete party.</p>',
        'order': 2,
        'is_featured': True
    },
    {
        'question': 'Are boat rides safe for children and non-swimmers?',
        'category': 'CHILDREN',
        'plain_answer': 'Absolutely. Every passenger is fitted with a marine-grade life jacket before stepping onto the jetty. Specialized child life jackets are provided.',
        'answer': '<p>Yes. Safety is our non-negotiable priority. All guests—regardless of swimming ability—wear properly fitted life jackets. Our boats are wide, stable aluminum hulls skippered by licensed local captains who maintain safe distances from hippos.</p>',
        'order': 3,
        'is_featured': True
    },
    {
        'question': 'What happens if the weather turns windy or rainy?',
        'category': 'WEATHER',
        'plain_answer': 'If lake conditions exceed safe operational limits, Nova will reschedule your departure or provide a 100% refund without penalty.',
        'answer': '<p>Lake Naivasha can develop sudden afternoon winds. Our captains constantly monitor water conditions. If conditions are unsafe, we delay departure or reschedule. If you cannot reschedule, you receive a full refund.</p>',
        'order': 4,
        'is_featured': True
    },
    {
        'question': 'How do I get to Crescent Island by boat?',
        'category': 'CRESCENT',
        'plain_answer': 'Nova boats drop you at Crescent Island\'s private western jetty. A sanctuary guide leads your walking safari, and your boat waits to bring you back.',
        'answer': '<p>Taking a boat is the most scenic way to visit Crescent Island. We cruise past hippo pods across the bay, dock at the island jetty, and your captain remains moored while you enjoy the guided walking circuit.</p>',
        'order': 5,
        'is_featured': True
    },
    {
        'question': 'How far in advance should I book my ride?',
        'category': 'BOOKING',
        'plain_answer': 'We recommend booking 24 hours in advance for hotel pickups and sunset cruises. Same-day bookings are accepted subject to boat availability.',
        'answer': '<p>For standard departures from Nova Lake Base, 2–4 hours advance notice is usually sufficient. For hotel jetty departures, boat positioning, or sunset cruises, 24 hours notice ensures your preferred time slot is secured.</p>',
        'order': 6,
        'is_featured': True
    }
]

for fdata in faqs_data:
    QuestionAnswer.objects.update_or_create(question=fdata['question'], defaults=fdata)
print(f"[OK] Seeded {len(faqs_data)} FAQs.")

# 10. GUIDE ARTICLES
articles_data = [
    {
        'title': 'Nairobi to Lake Naivasha: Travel Times, Routes & Transport Options',
        'slug': 'nairobi-to-naivasha-travel-guide',
        'category': 'PLANNING',
        'excerpt': 'Everything you need to know about driving, taking an Uber, using a Matatu, or riding the SGR train from Nairobi down the Great Rift Valley to Lake Naivasha.',
        'body': 'Traveling the 90 kilometers from Nairobi to Lake Naivasha is one of Kenya\'s classic scenic journeys. Taking the A104 Nairobi-Nakuru highway down the escarpment takes approximately 1.5 to 2 hours in normal traffic. Make sure to stop at the Great Rift Valley viewpoint on the descent.',
        'direct_quick_answer': 'The drive from Nairobi to Lake Naivasha takes 1.5 to 2 hours via the A104 highway. A private taxi costs KES 5,000–7,000, while public matatus cost KES 350–450 departing from Nyamakima in Nairobi.',
        'is_featured': True,
    },
    {
        'title': 'Best Time for a Lake Naivasha Boat Ride: Morning vs Sunset',
        'slug': 'best-time-boat-ride-naivasha',
        'category': 'PLANNING',
        'excerpt': 'Why morning rides offer glassy water and active bird hunting, while 5:00 PM sunset departures deliver dramatic Rift Valley golden hour light.',
        'body': 'Morning departures (between 07:00 AM and 09:30 AM) deliver the calmest lake water with virtually no wind chop. African fish eagles and kingfishers hunt actively during these hours. Sunset departures (17:00) offer spectacular photography as hippos begin emerging onto shores.',
        'direct_quick_answer': 'Early morning (07:00–09:30 AM) is best for glassy calm water and bird watching. Late afternoon (17:00–18:30) is best for dramatic Rift Valley sunset views and hippo photography.',
        'is_featured': True,
    },
    {
        'title': 'Lake Naivasha Boat Ride Safety: Captain Protocols & Life Jackets',
        'slug': 'lake-naivasha-boat-safety',
        'category': 'SAFETY',
        'excerpt': 'A transparent look at how Nova handles passenger safety, mandatory life jacket fitting, hippo buffer distances, and afternoon wind monitoring.',
        'body': 'Safety on Lake Naivasha requires experienced local knowledge. Hippos are territorial animals that must be given wide 30-meter buffers. Nova boats carry inspected marine-grade life vests for every passenger and avoid shallow mud-traps.',
        'direct_quick_answer': 'All Nova boat rides require certified life jacket wear. Captains maintain strict 30-meter minimum safety distances from hippo pods and hold valid local navigation licenses.',
        'is_featured': False,
    }
]

for adata in articles_data:
    GuideArticle.objects.update_or_create(slug=adata['slug'], defaults=adata)
print(f"[OK] Seeded {len(articles_data)} Guide Articles.")

print("\n=== NOVA PRODUCTION DATABASE READY ===")
