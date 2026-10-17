from datetime import date
from django.db import migrations
from django.utils.text import slugify


TOUR_GBP_METADATA = {
    'classic-lake-safari': {
        'branded_name': 'Nova Classic Lake Safari',
        'gbp_activity_name': '1-Hour Boat Ride on Lake Naivasha',
        'primary_intent': 'Core lake/boat',
        'audience_tags': 'first-time visitors, couples, families, friends, day-trippers',
        'review_prompt': 'What did you enjoy most about your Lake Naivasha boat ride today?',
        'direct_answer': (
            'Explore Lake Naivasha on a guided 60-minute boat ride with a local captain from Nova Karagita Base '
            'or an approved hotel jetty. Available as a private boat (up to 7 guests) or shared seats, this ride '
            'covers scenic shoreline routes with opportunities to see hippos, African fish eagles, pelicans and '
            'water birds. Best suited for first-time visitors, couples, families and travellers on a day trip.'
        ),
    },
    'hippo-bird-safari': {
        'branded_name': 'Nova Hippo & Bird Safari',
        'gbp_activity_name': 'Lake Naivasha Hippo & Bird Safari',
        'primary_intent': 'Boat safari / hippos / birds',
        'audience_tags': 'wildlife lovers, nature travellers, families, couples, birders',
        'review_prompt': 'What wildlife did you enjoy seeing most today?',
        'direct_answer': (
            'Discover the wildlife of Lake Naivasha on a private guided boat safari focused on resident hippo pods '
            'and water birds. Over 120 minutes on the water (up to 7 guests per boat), your local captain navigates '
            'shallow papyrus bays where African fish eagles, kingfishers, pelicans, cormorants and herons are '
            'commonly seen at safe observation distances.'
        ),
    },
    'crescent-island': {
        'branded_name': 'Nova Crescent Island Boat Transfer & Walking Tour',
        'gbp_activity_name': 'Crescent Island Boat Ride & Walking Safari',
        'primary_intent': 'Crescent Island',
        'audience_tags': 'walking safari guests, families, couples, Nairobi day-trippers',
        'review_prompt': 'What did you enjoy most about the boat ride and Crescent Island?',
        'direct_answer': (
            'Travel across Lake Naivasha by private boat to Crescent Island Game Sanctuary, combining a scenic '
            'wildlife crossing with standby boat return after your walking safari. Nova’s boat rate covers the '
            'private crossing and captain standby for up to 7 guests; Crescent Island sanctuary entry fees are '
            'separate third-party charges paid directly at the island gate.'
        ),
    },
    'sunset-cruise': {
        'branded_name': 'Nova Sunset Lake Cruise',
        'gbp_activity_name': 'Lake Naivasha Sunset Boat Cruise',
        'primary_intent': 'Sunset / couples / photography',
        'audience_tags': 'couples, photographers, small private groups, sundowner guests',
        'review_prompt': 'What did you enjoy most about the sunset trip?',
        'direct_answer': (
            'Experience Lake Naivasha during golden hour on a 90-minute private sunset boat cruise for up to 7 guests. '
            'Designed for couples, photographers and small private groups, this late-afternoon departure focuses on '
            'calmer evening light, Rift Valley reflections and shoreline birdlife, subject to safe afternoon wind '
            'and weather conditions.'
        ),
    },
    'private-charter': {
        'branded_name': 'Nova Private Lake Charter',
        'gbp_activity_name': 'Private Lake Naivasha Boat Ride – 2 Hours',
        'primary_intent': 'Private / high-value',
        'audience_tags': 'couples, families, photographers, small private groups',
        'review_prompt': 'What did you like most about having the private boat?',
        'direct_answer': (
            'Enjoy Lake Naivasha with your own private boat and dedicated captain for up to 7 guests. Choose between '
            'hourly or extended full-day private charter options for flexible pacing, unhurried wildlife stops, '
            'custom photography positioning or quiet time on the water with your group.'
        ),
    },
    'family-ride': {
        'branded_name': 'Nova Family Lake Explorer',
        'gbp_activity_name': 'Family Boat Ride on Lake Naivasha',
        'primary_intent': 'Family / kids / things to do',
        'audience_tags': 'families, parents with children, multi-generational groups',
        'review_prompt': 'What did your family enjoy most?',
        'direct_answer': (
            'A private, relaxed Lake Naivasha boat ride tailored for families and mixed-age groups of up to 7 guests. '
            'Includes dedicated child and adult life-jacket fitting before boarding, calm-water routing when '
            'conditions allow, and engaging commentary on hippos, fish eagles and lake ecology.'
        ),
    },
    'photography-birding': {
        'branded_name': 'Nova Birding & Creative Photography Charter',
        'gbp_activity_name': 'Lake Naivasha Bird Watching & Photography Tour',
        'primary_intent': 'Birding / photography',
        'audience_tags': 'birders, wildlife photographers, filmmakers, nature enthusiasts',
        'review_prompt': 'Which birds or photographic moments stood out most on your trip?',
        'direct_answer': (
            'A slower-paced 180-minute specialist boat charter on Lake Naivasha limited to 1–4 guests for unobstructed '
            'camera angles and stability. Your captain positions the boat for optimal light and sightings of African '
            'fish eagles, malachite and pied kingfishers, goliath herons, pelicans and hippos.'
        ),
    },
    'groups-events': {
        'branded_name': 'Nova Corporate & Group Lake Regatta',
        'gbp_activity_name': 'Private Group Boat Tour on Lake Naivasha',
        'primary_intent': 'Groups / corporate / friends',
        'audience_tags': 'corporate teams, friends, extended families, schools, organised groups',
        'review_prompt': 'How was the coordination and lake experience for your group?',
        'direct_answer': (
            'A coordinated multi-boat Lake Naivasha experience for groups of 10 to 50 guests, suited for corporate '
            'retreats, friends, extended families and school outings. Nova organises synchronized departures, '
            'passenger boat allocation across licensed captains, and life-jacket briefings from Karagita Base '
            'or approved partner jetties.'
        ),
    },
    'sunrise-wildlife': {
        'branded_name': 'Nova Sunrise Wildlife Boat Ride',
        'gbp_activity_name': 'Lake Naivasha Sunrise Boat Ride',
        'primary_intent': 'Sunrise / birding',
        'audience_tags': 'early risers, birders, photographers, couples',
        'review_prompt': 'What did you enjoy most about the early morning lake conditions?',
        'direct_answer': (
            'Start the day with an early-morning boat experience on Lake Naivasha built around quiet water, '
            'morning light, bird activity and photography. Subject to operational verification and safe launch conditions.'
        ),
    },
    'full-lake-explorer': {
        'branded_name': 'Nova Full Lake Explorer',
        'gbp_activity_name': 'Lake Naivasha Full Lake Explorer',
        'primary_intent': 'Tour / excursion',
        'audience_tags': 'explorers, full-day visitors, nature enthusiasts',
        'review_prompt': 'What part of the extended lake route did you enjoy most?',
        'direct_answer': (
            'An extended Lake Naivasha boat route covering multiple shoreline habitats, papyrus bays and open-water '
            'scenery, subject to operational verification and weather conditions.'
        ),
    },
}

GBP_CANONICAL_SERVICES = [
    (
        1,
        'Boat Ride on Lake Naivasha',
        'Enjoy a guided boat ride on Lake Naivasha with beautiful lake scenery and opportunities to see hippos, African fish eagles, pelicans and other water birds. Suitable for couples, families, friends and visitors exploring Naivasha.',
        'Core lake/boat',
        1,
        'classic-lake-safari',
        '',
    ),
    (
        2,
        'Lake Naivasha Boat Ride',
        'Explore Lake Naivasha by boat with a local captain who knows the lake, wildlife areas and scenic routes. Choose from shorter sightseeing rides or longer experiences depending on your time, group size and interests.',
        'Core lake/boat',
        1,
        '',
        'tours:tour_list',
    ),
    (
        3,
        'Boat Rides Naivasha',
        'Nova offers boat rides in Naivasha for individuals, couples, families and groups. Enjoy wildlife viewing, bird watching and views across Lake Naivasha, with private and shared boat options available depending on your preferred experience.',
        'Core lake/boat',
        1,
        '',
        'tours:tour_list',
    ),
    (
        4,
        'Lake Naivasha Boat Safari',
        'Experience a wildlife-focused boat safari on Lake Naivasha. Cruise through areas known for hippos and birdlife while enjoying views of the lake, surrounding hills and shoreline. A great option for visitors interested in nature and photography.',
        'Wildlife / safari',
        4,
        'hippo-bird-safari',
        '',
    ),
    (
        5,
        'Lake Naivasha Boat Tour',
        'Take a guided boat tour of Lake Naivasha and discover the lake from the water. Your captain will help you spot wildlife, birds and interesting parts of the shoreline while explaining more about the lake and the surrounding area.',
        'Tour / excursion',
        2,
        '',
        'tours:tour_list',
    ),
    (
        6,
        'Lake Naivasha Hippo Boat Tour',
        'Join a Lake Naivasha hippo boat tour and explore areas where hippos are commonly seen in their natural environment. The trip can also include bird watching and sightings of African fish eagles, pelicans and other water birds.',
        'Wildlife / safari',
        4,
        'hippo-bird-safari',
        '',
    ),
    (
        7,
        'Crescent Island Boat Ride',
        'Travel across Lake Naivasha by boat to Crescent Island. Enjoy wildlife and bird sightings during the crossing before arriving at the island for an optional walking safari. Crescent Island entrance fees are separate unless specifically included.',
        'Crescent Island',
        3,
        'crescent-island',
        '',
    ),
    (
        8,
        'Crescent Island Boat Transfer',
        'Book a boat transfer between the Lake Naivasha departure point and Crescent Island. The crossing also gives you an opportunity to enjoy lake scenery, birds and wildlife before or after your Crescent Island walking safari.',
        'Crescent Island',
        3,
        'crescent-island',
        '',
    ),
    (
        9,
        'Private Lake Naivasha Boat Ride',
        'Enjoy Lake Naivasha with your own private boat and captain. Private rides are ideal for couples, families, photographers and small groups who want more flexibility with their route, pace, wildlife viewing and time on the water.',
        'Audience / private',
        5,
        'private-charter',
        '',
    ),
    (
        10,
        'Lake Naivasha Sunset Boat Ride',
        'Experience Lake Naivasha during golden hour and sunset. Enjoy cooler evening temperatures, reflections across the water and changing colours over the lake. A popular choice for couples, photographers and private groups.',
        'Sunset / couples',
        5,
        'sunset-cruise',
        '',
    ),
    (
        11,
        'Lake Naivasha Sunrise Boat Ride',
        'Start the day with an early morning boat ride on Lake Naivasha. Sunrise trips offer peaceful lake conditions, beautiful morning light and excellent opportunities for bird watching, wildlife viewing and photography.',
        'Sunrise / birding',
        5,
        'sunrise-wildlife',
        'tours:tour_list',
    ),
    (
        12,
        'Lake Naivasha Bird Watching Tour',
        'Explore the birdlife of Lake Naivasha from the water. Look out for African fish eagles, pelicans, cormorants, kingfishers and other species with help from a local captain familiar with the lake’s birding areas.',
        'Wildlife / birding',
        4,
        'photography-birding',
        '',
    ),
    (
        13,
        'Lake Naivasha Photography Boat Tour',
        'A slower-paced Lake Naivasha boat experience designed for photographers and wildlife enthusiasts. Spend more time positioning for photographs of birds, hippos, landscapes, reflections and other scenes around the lake.',
        'Birding / photography',
        5,
        'photography-birding',
        '',
    ),
    (
        14,
        'Family Boat Ride Naivasha',
        'Enjoy a relaxed Lake Naivasha boat ride suitable for families visiting Naivasha. Children and adults can enjoy wildlife sightings, bird watching and beautiful lake scenery while exploring the lake with an experienced local captain.',
        'Audience / family',
        5,
        'family-ride',
        '',
    ),
    (
        15,
        'Group Boat Ride Naivasha',
        'Boat rides for groups of friends, families, schools, organisations and corporate teams visiting Lake Naivasha. Nova can coordinate multiple guests and boats depending on the size of the group and the type of experience required.',
        'Audience / groups',
        5,
        'groups-events',
        '',
    ),
    (
        16,
        'Hotel Boat Pickup Naivasha',
        'Selected hotels and lakeside properties may allow guests to begin their Lake Naivasha boat experience directly from the hotel or nearby waterfront access. Availability depends on the property, lake conditions and prior arrangements.',
        'Hotel access',
        5,
        '',
        'partners:hotel_hub',
    ),
]

GBP_POST_THEMES = [
    (1, 1, 'Lake Naivasha Boat Ride Overview', 'Core lake/boat', 'Explore Lake Naivasha on a 1-hour private or shared boat ride from Karagita Base.', 'classic-lake-safari', ''),
    (1, 2, 'Crescent Island Crossing & Walking Safari', 'Crescent Island', 'Cross Lake Naivasha by boat to Crescent Island with full return standby and clear gate-fee breakdown.', 'crescent-island', ''),
    (1, 3, 'Hippo & Bird Safari on Lake Naivasha', 'Wildlife / safari', '2-hour guided boat safari exploring shallow papyrus bays for hippos, fish eagles and water birds.', 'hippo-bird-safari', ''),
    (2, 1, 'Things to Do in Naivasha: Lake Tours', 'Tour / attraction', 'Planning a trip to Naivasha? Compare guided lake tours, durations and transparent options.', '', 'tours:tour_list'),
    (2, 2, 'Family Boat Ride on Lake Naivasha', 'Audience / family', 'Child and adult fitted life jackets, calm-water routing and engaging wildlife commentary for families.', 'family-ride', ''),
    (2, 3, 'Private Lake Naivasha Boat Charter', 'Audience / private', 'Reserve your own boat and captain for flexible pacing, photography and quiet time on the water.', 'private-charter', ''),
    (3, 1, 'Golden Hour Sunset Cruise on Lake Naivasha', 'Sunset / couples', 'Evening reflections and Rift Valley light on a 90-minute private sunset boat cruise.', 'sunset-cruise', ''),
    (3, 2, 'Bird Watching & African Fish Eagles', 'Wildlife / birding', 'Specialist 3-hour birding and photography charter for kingfishers, fish eagles, herons and pelicans.', 'photography-birding', ''),
    (3, 3, 'Lake Naivasha Boat Ride Prices & Planning', 'Price / cost', 'Compare per-boat and per-person options, Crescent Island gate fees and hotel positioning policies.', '', 'core:prices'),
    (4, 1, 'Couples & Private Lake Experiences', 'Audience / couples', 'Quiet private boat charters and golden-hour sunset cruises for couples visiting Naivasha.', 'sunset-cruise', ''),
    (4, 2, 'Combining a Lake Boat Ride with Crescent Island', 'Crescent Island', 'How to plan your boat transfer and walking safari time on Crescent Island.', 'crescent-island', ''),
    (4, 3, 'Nairobi to Lake Naivasha Day-Trip Planning', 'Trip planning', 'Morning vs afternoon departure timing, driving routes from Nairobi and what to bring on the boat.', '', 'core:plan_naivasha'),
]


def forwards(apps, schema_editor):
    Tour = apps.get_model('tours', 'Tour')
    GBPService = apps.get_model('tours', 'GBPService')
    GBPQueryScorecard = apps.get_model('tours', 'GBPQueryScorecard')
    GBPPostTheme = apps.get_model('tours', 'GBPPostTheme')
    SiteSettings = apps.get_model('core', 'SiteSettings')
    BusinessFact = apps.get_model('core', 'BusinessFact')
    ClaimEvidence = apps.get_model('core', 'ClaimEvidence')
    GuideArticle = apps.get_model('content', 'GuideArticle')

    today = date(2026, 10, 16)

    # 1. Seed canonical BusinessFact & ClaimEvidence records
    settings_obj = SiteSettings.objects.first()
    facts = [
        ('business-name', 'Business Name', settings_obj.business_name if settings_obj else 'Nova Boat Rides Naivasha', 'Official Registration & GBP'),
        ('phone-display', 'Primary Phone', settings_obj.phone_display if settings_obj else '+254 701 215 295', 'Nova Operations Desk'),
        ('phone-e164', 'Phone (E.164)', settings_obj.phone_e164 if settings_obj else '+254701215295', 'Nova Operations Desk'),
        ('whatsapp-number', 'WhatsApp Number', settings_obj.whatsapp_number if settings_obj else '254701215295', 'Nova WhatsApp Dispatch'),
        ('email', 'Official Email', settings_obj.email if settings_obj else 'hello@novaboatridesnaivasha.co.ke', 'Nova Operations Desk'),
        ('street-address', 'Street Address', settings_obj.street_address if settings_obj else 'Karagita Beach, Moi South Lake Road', 'GPS & Site Survey'),
        ('locality', 'Locality', settings_obj.locality if settings_obj else 'Karagita, Naivasha', 'GPS & Site Survey'),
        ('operating-hours', 'Operating Hours', settings_obj.operating_hours if settings_obj else 'Daily 6:30 AM – 6:30 PM', 'Operations Schedule'),
        ('coordinates', 'Launch Coordinates', '-0.762030, 36.425790', 'Karagita Jetty GPS Fix'),
        ('website-url', 'Primary Website URL', 'https://www.novaboatridesnaivasha.co.ke/', 'Canonical Domain Configuration'),
        ('gbp-website-url', 'GBP Website Attribution URL', 'https://www.novaboatridesnaivasha.co.ke/?utm_source=google&utm_medium=organic&utm_campaign=gbp_website&utm_content=home', 'GBP UTM Taxonomy §5.4'),
    ]
    for key, label, val, src in facts:
        BusinessFact.objects.update_or_create(
            key=key,
            defaults={
                'public_label': label,
                'value': val,
                'last_verified_at': today,
                'verification_source': src,
                'active': True,
            },
        )

    claims = [
        (
            'crescent-island-tariff-2026',
            'Crescent Island Game Sanctuary entrance fees are third-party charges paid directly at the sanctuary gate (Citizen Adult KES 800 / Child KES 400; Resident Adult KES 1,100 / Child KES 550; Non-Resident Adult USD 33 / Child USD 16 / Student USD 22).',
            'OFFICIAL_TARIFF',
            'https://www.crescentisland.co/ Official 2026 Tariff Schedule',
            True,
        ),
        (
            'life-jacket-safety-policy',
            'Adult and child life jackets are fitted before departure and mandatory while on open water.',
            'OPERATIONAL_LOG',
            'Nova Karagita Base Boarding Standard Operating Procedure',
            True,
        ),
        (
            'wildlife-observation-policy',
            'Wildlife is wild; sightings vary by weather, water level and time of day, and are never guaranteed.',
            'OPERATIONAL_LOG',
            'Nova Responsible Wildlife Viewing Policy',
            True,
        ),
    ]
    for c_key, c_text, e_type, e_ref, pub in claims:
        ClaimEvidence.objects.update_or_create(
            claim_key=c_key,
            defaults={
                'claim_text': c_text,
                'evidence_type': e_type,
                'evidence_reference': e_ref,
                'verified_at': today,
                'publishable': pub,
            },
        )

    # 2. Enrich Tour records with GBP & AEO metadata
    tours_by_slug = {t.slug: t for t in Tour.objects.all()}
    for slug, meta in TOUR_GBP_METADATA.items():
        tour = tours_by_slug.get(slug)
        if tour:
            tour.branded_name = meta['branded_name']
            tour.gbp_activity_name = meta['gbp_activity_name']
            tour.primary_intent = meta['primary_intent']
            tour.audience_tags = meta['audience_tags']
            tour.review_prompt = meta['review_prompt']
            tour.direct_answer = meta['direct_answer']
            tour.save(update_fields=[
                'branded_name', 'gbp_activity_name', 'primary_intent',
                'audience_tags', 'review_prompt', 'direct_answer'
            ])

    # 3. Seed 16 Canonical GBP Services (§5.5)
    for num, name, desc, cluster, wave, act_slug, dest_name in GBP_CANONICAL_SERVICES:
        act = tours_by_slug.get(act_slug) if act_slug else None
        GBPService.objects.update_or_create(
            number=num,
            defaults={
                'name': name,
                'slug': slugify(name),
                'description': desc,
                'primary_cluster': cluster,
                'wave': wave,
                'activity': act,
                'destination_name': dest_name,
                'show_price_in_gbp': False,
                'is_active': True,
                'last_verified_at': today,
            },
        )

    # 4. Seed GBP Monthly Scorecards (§1.2 & §12.5)
    GBPQueryScorecard.objects.update_or_create(
        period_label='Njovic Market Benchmark (§1.2)',
        defaults={
            'period_start': date(2026, 9, 1),
            'unique_discovery_queries': 15,
            'lake_naivasha_boat_ride_searches': 78,
            'boat_ride_on_lake_naivasha_searches': 57,
            'lake_naivasha_tour_searches': 33,
            'tourist_attraction_naivasha_searches': 72,
            'crescent_island_searches': 20,
            'boat_safari_hippo_searches': 21,
            'price_cost_searches': 20,
            'family_couple_group_searches': 16,
            'notes': 'Reference benchmark from PRD §1.2 showing achievable local query breadth across clusters.',
        },
    )
    GBPQueryScorecard.objects.update_or_create(
        period_label='Baseline (Oct 2026)',
        defaults={
            'period_start': today,
            'unique_discovery_queries': 3,
            'lake_naivasha_boat_ride_searches': 12,
            'boat_ride_on_lake_naivasha_searches': 8,
            'lake_naivasha_tour_searches': 0,
            'tourist_attraction_naivasha_searches': 0,
            'crescent_island_searches': 4,
            'boat_safari_hippo_searches': 3,
            'price_cost_searches': 5,
            'family_couple_group_searches': 2,
            'notes': 'Nova initial baseline: top-3 for Boat Ride Naivasha; expanding into Wave 1-5 clusters.',
        },
    )

    # 5. Seed 12 Rotating GBP Post Cadence Themes (§10.3)
    for week, order, title, cluster, summary, act_slug, dest_name in GBP_POST_THEMES:
        act = tours_by_slug.get(act_slug) if act_slug else None
        GBPPostTheme.objects.update_or_create(
            slug=slugify(f"w{week}-{order}-{title}"),
            defaults={
                'week_number': week,
                'post_order': order,
                'theme_title': title,
                'target_cluster': cluster,
                'suggested_summary': summary,
                'activity': act,
                'destination_name': dest_name,
                'is_active': True,
            },
        )

    # 6. Link GuideArticles to their primary bookable activity (§11.1)
    for article in GuideArticle.objects.all():
        slug_lower = (article.slug or '').lower()
        target_slug = 'classic-lake-safari'
        if 'crescent' in slug_lower:
            target_slug = 'crescent-island'
        elif any(k in slug_lower for k in ('bird', 'photo')):
            target_slug = 'photography-birding'
        elif any(k in slug_lower for k in ('hippo', 'safari', 'wildlife')):
            target_slug = 'hippo-bird-safari'
        elif any(k in slug_lower for k in ('family', 'children')):
            target_slug = 'family-ride'
        elif any(k in slug_lower for k in ('romantic', 'couple', 'sunset', 'timing')):
            target_slug = 'sunset-cruise'
        elif any(k in slug_lower for k in ('group', 'corporate', 'team')):
            target_slug = 'groups-events'
        elif any(k in slug_lower for k in ('private', 'full-day')):
            target_slug = 'private-charter'
        target_tour = tours_by_slug.get(target_slug)
        if target_tour and article.related_activity_id != target_tour.pk:
            article.related_activity = target_tour
            article.save(update_fields=['related_activity'])


def backwards(apps, schema_editor):
    GBPService = apps.get_model('tours', 'GBPService')
    GBPQueryScorecard = apps.get_model('tours', 'GBPQueryScorecard')
    GBPPostTheme = apps.get_model('tours', 'GBPPostTheme')
    BusinessFact = apps.get_model('core', 'BusinessFact')
    ClaimEvidence = apps.get_model('core', 'ClaimEvidence')
    GBPService.objects.all().delete()
    GBPQueryScorecard.objects.all().delete()
    GBPPostTheme.objects.all().delete()
    BusinessFact.objects.all().delete()
    ClaimEvidence.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_businessfact_claimevidence_externalfee_disclaimer'),
        ('tours', '0006_gbpqueryscorecard_tour_audience_tags_and_more'),
        ('content', '0006_guidearticle_related_activity_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
