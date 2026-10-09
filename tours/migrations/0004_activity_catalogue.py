from decimal import Decimal
from django.db import migrations, models
from django.utils.text import slugify


CATALOGUE = [
    ('classic-lake-safari', '1-Hour Boat Ride on Lake Naivasha', 'wildlife', 60,
     'A guided introduction to Lake Naivasha, with time for scenery and opportunities to observe hippos and birds.'),
    ('hippo-bird-safari', 'Lake Naivasha Hippo & Bird Safari', 'wildlife', 90,
     'A wildlife-focused boat safari with time to observe lake habitats and birdlife. Sightings depend on the day and conditions.'),
    ('crescent-island', 'Crescent Island Boat Ride & Walking Safari', 'crescent', 120,
     'Combine a return boat crossing with a visit to Crescent Island. Nova boat charges and sanctuary admission are shown separately.'),
    ('sunset-cruise', 'Lake Naivasha Sunset Boat Cruise', 'sunrise-sunset', 90,
     'An evening lake cruise for golden-hour scenery and photography, subject to weather and safe departure conditions.'),
    ('private-charter', 'Private Lake Naivasha Boat Ride', 'private', 120,
     'Reserve a boat for your party. Choose an available charter duration and discuss the route with the Nova team.'),
    ('family-ride', 'Family Boat Ride on Lake Naivasha', 'family', 75,
     'A lake outing for families. Confirm suitable life jackets, boarding needs and the selected option before departure.'),
    ('photography-birding', 'Lake Naivasha Bird Watching & Photography Boat Tour', 'birding', 150,
     'A focused lake session for birders and photographers, with time for observation and positioning when conditions allow.'),
    ('groups-events', 'Private Group & Corporate Boat Tour on Lake Naivasha', 'groups', 120,
     'Plan a lake outing for your group. Boat allocation, passenger limits, departure logistics and final price require confirmation.'),
    ('sunrise-wildlife', 'Lake Naivasha Sunrise Wildlife Boat Ride', 'sunrise-sunset', 90,
     'A proposed early-morning lake experience for wildlife observation and soft-light photography.'),
    ('full-lake-explorer', 'Lake Naivasha Full Lake Explorer', 'wildlife', 180,
     'A proposed extended lake experience with a defined route through several habitats, subject to operational verification.'),
]

PRIMARY = [
 ('Boat Rides Naivasha', '', 'wildlife'), ('Boat Ride on Lake Naivasha', 'classic-lake-safari', 'wildlife'),
 ('Lake Naivasha Boat Ride', '', 'wildlife'), ('Lake Naivasha Boat Safari', 'hippo-bird-safari', 'wildlife'),
 ('Boat Safari Naivasha', 'hippo-bird-safari', 'wildlife'), ('Lake Naivasha Boat Tour', 'full-lake-explorer', 'wildlife'),
 ('Crescent Island Boat Ride', 'crescent-island', 'crescent'), ('Lake Naivasha Hippo Boat Tour', 'hippo-bird-safari', 'wildlife'),
 ('Private Lake Naivasha Boat Ride', 'private-charter', 'private'), ('Lake Naivasha Sunset Boat Cruise', 'sunset-cruise', 'sunrise-sunset'),
 ('Lake Naivasha Sunrise Boat Ride', 'sunrise-wildlife', 'sunrise-sunset'), ('Family Boat Ride Naivasha', 'family-ride', 'family'),
 ('Lake Naivasha Bird Watching Boat Tour', 'photography-birding', 'birding'), ('Lake Naivasha Photography Boat Tour', 'photography-birding', 'birding'),
 ('Private Group Boat Tour Lake Naivasha', 'groups-events', 'groups'),
]
SECONDARY = [
 ('1-Hour Lake Naivasha Boat Ride', 'classic-lake-safari', 'wildlife'), ('Crescent Island Boat Transfer', 'crescent-island', 'crescent'),
 ('Couples Boat Ride Lake Naivasha', 'private-charter', 'private'), ('Romantic Boat Ride Naivasha', 'sunset-cruise', 'private'),
 ('Birthday Boat Ride Naivasha', 'private-charter', 'private'), ('Anniversary Boat Ride Naivasha', 'private-charter', 'private'),
 ('Group Boat Ride Naivasha', 'groups-events', 'groups'), ('Corporate Boat Tour Naivasha', 'groups-events', 'groups'),
 ('Hotel Boat Pickup Naivasha', '', 'hotel'), ('Hotel-Origin Lake Naivasha Boat Ride', '', 'hotel'),
 ('Lake Naivasha Wildlife Boat Tour', 'hippo-bird-safari', 'wildlife'), ('Lake Naivasha Scenic Boat Cruise', 'full-lake-explorer', 'wildlife'),
 ('Early Morning Lake Naivasha Boat Tour', 'sunrise-wildlife', 'sunrise-sunset'), ('Lake Naivasha Extended Boat Tour', 'full-lake-explorer', 'wildlife'),
 ('Lake Naivasha Bird Photography Safari', 'photography-birding', 'birding'),
]


def forwards(apps, schema_editor):
    Tour = apps.get_model('tours', 'Tour')
    Rate = apps.get_model('tours', 'ExperienceRate')
    Option = apps.get_model('tours', 'TourOption')
    Detail = apps.get_model('tours', 'ActivityDetail')
    FAQ = apps.get_model('tours', 'ActivityFAQ')
    Step = apps.get_model('tours', 'ItineraryStep')
    Image = apps.get_model('tours', 'ActivityImage')
    Intent = apps.get_model('tours', 'ServiceIntent')
    Fee = apps.get_model('core', 'ExternalFee')
    # Preserve the existing public catalogue. New publications must pass the new checklist.
    Tour.objects.filter(is_active=True).update(status='PUBLISHED', legacy_publication=True)
    for tour in Tour.objects.all():
        tour.duration_minutes = int(Decimal(str(tour.duration_hours)) * 60)
        tour.save(update_fields=['duration_minutes'])
    for order, (slug, name, category, proposed_minutes, summary) in enumerate(CATALOGUE):
        tour = Tour.objects.filter(slug=slug).first()
        is_new = tour is None
        if is_new:
            tour = Tour.objects.create(slug=slug, name=name, summary=summary, body=summary,
                duration_minutes=proposed_minutes, duration_hours=Decimal(proposed_minutes)/60,
                category=category, status='DRAFT', is_active=False, order=order)
        else:
            tour.internal_name = tour.name
            tour.legacy_body = tour.body
            tour.name = name
            tour.summary = summary
            tour.category = category
            tour.body = summary + '\n\nChoose a booking option for the exact duration and passenger limits. Wildlife sightings and route conditions vary. Our team confirms availability and departure arrangements before your ride.'
        tour.direct_answer = summary
        tour.seo_title = (name + ' | Nova')[:70]
        tour.meta_description = (summary + ' Check availability with Nova.')[:160]
        tour.meeting_point = 'Nova Karagita Base, Karagita Beach, Moi South Lake Road, Naivasha. Hotel departures require prior confirmation.'
        tour.what_to_bring = 'Sun protection\nDrinking water\nCamera if desired\nSecure footwear\nA light layer for early or late departures'
        tour.accessibility_notes = 'Contact Nova before booking to discuss mobility needs, boarding assistance and suitable life jackets. Step-free access is not assumed.'
        tour.safety_briefing = 'Follow your captain’s safety briefing and wear a properly fitted life jacket. Contact Nova to confirm equipment and boarding requirements for your party.'
        tour.child_policy = 'Tell Nova the ages of children before booking so suitable equipment and any child pricing can be confirmed.'
        tour.cancellation_policy = 'Ask Nova to confirm cancellation deadlines, deposit conditions and any applicable refund or rescheduling terms before accepting a quote.'
        tour.weather_policy = 'Departure and route depend on safe lake conditions. Nova will confirm any weather-related delay, alternative or cancellation and the applicable terms.'
        tour.inclusions = 'Boat and fuel for the selected option\nLocal captain\nFitted life jackets and safety briefing'
        tour.exclusions = 'Road transport and hotel positioning unless separately confirmed\nMeals and drinks unless expressly included\nThird-party admission fees unless expressly bundled'
        tour.save()
        for kind, texts in [('HIGHLIGHT', [summary, 'Local captain and lake commentary', 'Option-specific duration and passenger limits', 'Direct planning with Nova']),
                            ('INCLUDED', tour.inclusions.splitlines()), ('EXCLUDED', tour.exclusions.splitlines())]:
            for index, text in enumerate(texts):
                Detail.objects.get_or_create(tour=tour, kind=kind, order=index, defaults={'text':text})
        for index, (title, desc) in enumerate([
            ('Meet and prepare', 'Meet at the confirmed departure point for your briefing and life jacket fitting.'),
            ('Explore your route', 'Follow the route agreed for your selected option. Stops and wildlife observation vary with conditions.'),
            ('Return to the agreed point', 'Return to your confirmed landing point. The quoted duration describes your selected option.')]):
            Step.objects.get_or_create(tour=tour, order=index, defaults={'title':title, 'description':desc})
        questions = [
            ('How long is this experience?', 'Choose a booking option to see its exact duration. Confirm any walking time, transfers or extended stops with Nova.'),
            ('What is included in the price?', 'The selected option identifies the boat service. The included and excluded lists and any mandatory attraction fees are shown separately.'),
            ('Is my enquiry a confirmed booking?', 'No. Nova confirms availability, departure arrangements and final price before your booking is confirmed.'),
            ('Can children join?', tour.child_policy),
            ('Are wildlife sightings guaranteed?', 'No. Wildlife is wild; sightings vary with weather, water levels, time of day and animal movement.'),
            ('What happens if the weather changes?', tour.weather_policy),
            ('Can we depart from our hotel?', 'Ask Nova to check your hotel’s access, permissions, notice period and any positioning or transport charges.'),
        ]
        for index, (question, answer) in enumerate(questions):
            FAQ.objects.get_or_create(tour=tour, order=index, defaults={'question':question, 'answer':answer})
        if tour.image:
            Image.objects.get_or_create(tour=tour, is_primary=True, defaults={'image':tour.image.name,
                'webp_image':tour.webp_image.name or '', 'webp_mobile':tour.webp_mobile.name or '',
                'alt_text':name, 'role':'HERO', 'rights_confirmed':False})
        # Group matching currencies into the same actual option, without changing any stored monetary amount.
        grouped = {}
        for rate in Rate.objects.filter(experience=tour).order_by('id'):
            mode = 'GROUP' if category == 'groups' else ('SHARED' if rate.pricing_model == 'PER_PERSON' else 'PRIVATE')
            key = (rate.duration_minutes, rate.min_guests, rate.max_guests, mode)
            if key not in grouped:
                option = Option.objects.create(tour=tour,
                    name=f'{rate.duration_minutes}-minute {dict(SHARED="shared seats", PRIVATE="private boat", GROUP="group experience")[mode]}',
                    duration_minutes=rate.duration_minutes, min_guests=rate.min_guests, max_guests=rate.max_guests,
                    mode=mode, order=len(grouped))
                if category == 'crescent':
                    option.external_fees.set(Fee.objects.filter(provider_name__icontains='Crescent', is_active=True))
                grouped[key] = option
            rate.option = grouped[key]
            rate.save(update_fields=['option'])
    for level, rows in [('PRIMARY', PRIMARY), ('SECONDARY', SECONDARY)]:
        for index, (name, slug, category) in enumerate(rows):
            activity = Tour.objects.filter(slug=slug).first() if slug else None
            Intent.objects.get_or_create(slug=slugify(name), defaults={'name':name, 'level':level, 'category':category,
                'activity':activity, 'destination_name':'' if activity else ('partners:hotel_hub' if category == 'hotel' else 'tours:tour_list'),
                'description':'Discuss the appropriate experience and arrangements with Nova.', 'order':index})


class Migration(migrations.Migration):
    dependencies = [('tours', '0003_experiencerate_child_amount_and_more'), ('core', '0003_sitesettings_ga4_measurement_id_and_more')]
    operations = [migrations.AddField(model_name='tour', name='legacy_body', field=models.TextField(blank=True, editable=False)),
                  migrations.RunPython(forwards, migrations.RunPython.noop)]
