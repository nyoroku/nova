"""
Phase 10: Seeding new FAQs targeting the Phase 9 keyword clusters.
Targets keyword clusters and local pages:
- Families / Kids
- Honeymoon / Couples / Romance
- Corporate Team Building
- Photography Tours
- Birthday / Special Occasions
- Private Charter Hire
- Hell's Gate + Lake Combo
- Fishing Tours
- Oloidien Bay
- Hippo Point Area
Run: .venv\\Scripts\\python.exe seed_phase10_faqs.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import FAQ

def F(q, a, plain, intent, order):
    # Deduplicate: keep newest, delete extras
    dupes = FAQ.objects.filter(question=q)
    if dupes.count() > 1:
        keep = dupes.order_by('-id').first()
        dupes.exclude(id=keep.id).delete()
    faq, created = FAQ.objects.update_or_create(question=q, defaults={
        'answer': a, 'plain_answer': plain, 'search_intent': intent,
        'order': order, 'is_active': True, 'allow_indexing': True})
    print(f"  [{'NEW' if created else 'UPD'}] {q}")

faqs = [
    # 1. Families / Kids
    (
        "Are child-sized life jackets provided for the boat ride?",
        "<p><strong>Yes, absolutely!</strong> We provide properly fitted child-sized and infant life jackets. We believe child safety is non-negotiable, and every young passenger must wear a fitted jacket before the boat departs.</p>",
        "Yes, we provide properly fitted child-sized and infant life jackets to guarantee child safety.",
        "safety",
        501
    ),
    (
        "What is the minimum age for a child on the boat ride?",
        "<p>There is no minimum age. We welcome infants, toddlers, and older children. Our boats are spacious, flat-bottomed, and exceptionally stable, ensuring a comfortable experience for families with babies.</p>",
        "There is no minimum age limit. We welcome infants, toddlers, and children of all ages on our stable boats.",
        "safety",
        502
    ),
    (
        "Can a stroller fit on the Lake Naivasha safari boat?",
        "<p>While a stroller cannot be safely used or unfolded on the boat itself, you can easily store it in our secure beach office at Karagita Beach or leave it folded in our designated storage area on the larger boats.</p>",
        "Strollers cannot be unfolded on the boat, but we can safely store them at our Karagita Beach office or onboard in designated areas.",
        "logistics",
        503
    ),

    # 2. Honeymoon / Couples / Romance
    (
        "Can we book a private sunset boat ride for a marriage proposal?",
        "<p><strong>Yes, we love proposals!</strong> We can coordinate a private sunset cruise, arrange a chilled bottle of champagne, flowers, and even position the boat for a perfect golden hour proposal with the Rift Valley escarpment as your backdrop.</p>",
        "Yes, we coordinate private sunset cruises for marriage proposals, complete with champagne, flowers, and perfect photography setups.",
        "booking",
        504
    ),
    (
        "Is a romantic private charter boat ride expensive?",
        "<p>Not at all. Our private charters offer excellent value and cost-efficiency. You pay a simple, flat-rate per boat (not per person), meaning you get a dedicated captain and the entire vessel to yourselves for an intimate experience.</p>",
        "Our private charters are highly affordable. You pay a simple flat-rate per boat rather than a high per-person fee.",
        "pricing",
        505
    ),
    (
        "Are drinks and flowers allowed on a honeymoon boat ride?",
        "<p><strong>Yes, absolutely.</strong> You are more than welcome to bring your own drinks, snacks, and decorations, or you can request our team to pre-arrange a chilled bottle of wine, fresh flowers, and a fruit platter for your special ride.</p>",
        "Yes, you can bring your own drinks and decorations, or request our team to pre-arrange champagne and flowers.",
        "preparation",
        506
    ),

    # 3. Corporate Team Building
    (
        "How many people can your corporate team building boats accommodate?",
        "<p>Our total fleet can comfortably carry up to <strong>80+ passengers simultaneously</strong>. We coordinate multiple boats in convoy, maintaining radio contact so that all your team members enjoy the wildlife sighting at the same time.</p>",
        "Our fleet can accommodate up to 80+ people simultaneously in a coordinated multi-boat convoy.",
        "logistics",
        507
    ),
    (
        "Can we customize a full-day corporate retreat package?",
        "<p><strong>Yes!</strong> We design bespoke full-day corporate packages that combine morning boat safaris, walking tours on Crescent Island, team lunches at beautiful partner lakeside hotels, and cycling relays in Hell's Gate.</p>",
        "Yes, we design custom corporate day packages including boat safaris, Crescent Island walks, lunches, and Hell's Gate cycling.",
        "booking",
        508
    ),
    (
        "Do you provide KRA tax invoices for corporate bookings?",
        "<p><strong>Yes.</strong> Rafiki is a registered business entity. We issue fully compliant electronic tax invoices with our KRA PIN, ensuring a smooth procurement process for corporate retreats and company outings.</p>",
        "Yes, we provide fully compliant electronic KRA tax invoices for all corporate and group bookings.",
        "logistics",
        509
    ),

    # 4. Photography Tours
    (
        "What is the best lens to bring on a Lake Naivasha photography tour?",
        "<p>For spectacular bird and hippo portraits, we highly recommend a <strong>150-600mm or 100-400mm telephoto zoom lens</strong>. For wide escarpment landscapes and reflections, a 24-70mm lens is absolutely perfect.</p>",
        "A 150-600mm or 100-400mm telephoto zoom lens is best for wildlife, while a 24-70mm lens is ideal for wide landscapes.",
        "preparation",
        510
    ),
    (
        "Why is the early morning best for wildlife photography?",
        "<p>Between 6:30 AM and 8:30 AM, the low-angle sun creates warm, directional light, the lake is mirror-calm for reflections, and the wildlife (especially hippos and fish eagles) is at its peak activity level.</p>",
        "Early mornings offer warm low-angle light, a mirror-calm lake surface for reflections, and peak wildlife activity.",
        "timing",
        511
    ),
    (
        "Do you offer private photography boat tours?",
        "<p><strong>Yes.</strong> Our private photography charters are tailored for slow-paced viewing. The captain is trained to position the boat for optimal lighting, avoid sudden movements, and wait patiently for behavioral shots.</p>",
        "Yes, we offer dedicated private photography charters designed for slow-paced positioning and optimal lighting angles.",
        "booking",
        512
    ),

    # 5. Birthday / Special Occasions
    (
        "Can we bring a birthday cake and music speakers on the boat?",
        "<p>Yes, you are welcome to bring a birthday cake and play your favorite tunes via a portable Bluetooth speaker. We just ask that music is kept at a respectful volume to avoid disturbing the sensitive lake wildlife.</p>",
        "Yes, you can bring a cake and use a portable Bluetooth speaker at a respectful volume.",
        "preparation",
        513
    ),
    (
        "How do we coordinate a birthday boat ride party?",
        "<p>Simply message us on WhatsApp at <strong>+254 701 215 295</strong> with your guest count. We will reserve the boats, set up birthday greetings, coordinate any catering or cake delivery, and set up a lakeside table for your group.</p>",
        "Contact us on WhatsApp with your guest count, and we will coordinate boats, greetings, and lakeside table setups.",
        "booking",
        514
    ),
    (
        "Is there a lakeside venue for birthday lunches after the boat ride?",
        "<p><strong>Yes</strong>, Karagita Beach has a lively fish market serving fresh lakeside grilled tilapia and ugali. Alternatively, we can drop your party off at a luxury lakeside hotel jetty for a high-end birthday lunch.</p>",
        "Yes, you can enjoy fresh grilled tilapia at Karagita Beach or be dropped off at a lakeside hotel jetty for a birthday lunch.",
        "amenities",
        515
    ),

    # 6. Private Charter Hire
    (
        "What is included in a private boat hire with Rafiki?",
        "<p>A private charter includes exclusive use of the boat, a certified captain/wildlife guide, life jackets for all passengers, fuel, customizable routes, and expert commentary. There are no broker commissions.</p>",
        "A private hire includes the exclusive boat, certified guide/captain, life jackets, fuel, custom route, and wildlife commentary.",
        "booking",
        516
    ),
    (
        "Is booking in advance required for private boat hire?",
        "<p>While we welcome walk-ins at Karagita Beach, we highly recommend booking your private charter at least 24 hours in advance to guarantee your preferred time slot, especially during weekends and public holidays.</p>",
        "Booking in advance is highly recommended to secure your preferred slot, especially on weekends and holidays.",
        "booking",
        517
    ),
    (
        "Can we change our itinerary during a private boat hire?",
        "<p><strong>Yes, absolutely!</strong> That is the primary benefit of a private charter. You can ask the captain to spend more time with the hippos, focus on birding, or change routes as wildlife sightings occur.</p>",
        "Yes, you have full flexibility to adjust your route or focus with the captain during your private charter.",
        "booking",
        518
    ),

    # 7. Hell's Gate + Lake Combo
    (
        "How do I coordinate a Hell's Gate and Lake Naivasha combo tour?",
        "<p>We recommend cycling and hiking in Hell's Gate in the cool morning (8:00 AM - 12:00 PM), enjoying a fresh tilapia lunch at Karagita Beach, and taking your relaxing wildlife boat safari in the afternoon (2:00 PM - 4:00 PM).</p>",
        "We recommend visiting Hell's Gate in the morning for cycling/hiking and taking the boat safari in the afternoon after lunch.",
        "logistics",
        519
    ),
    (
        "Is cycling safe at Hell's Gate on a combo tour?",
        "<p><strong>Yes</strong>, Hell's Gate is very safe for cycling. There are no lions or leopards, and the herds of zebras, giraffes, and gazelles are well-accustomed to cyclists. We recommend staying on the designated trails.</p>",
        "Yes, cycling is highly safe as the park has no large predators and the herbivores are peaceful and used to visitors.",
        "safety",
        520
    ),
    (
        "Can we hire a single guide for both Hell's Gate and the boat ride?",
        "<p>Yes, Rafiki can coordinate a dedicated guide to accompany you from the park gates of Hell's Gate through the gorge, and then captain your private safari boat on Lake Naivasha for a seamless experience.</p>",
        "Yes, we can coordinate a seamless guided experience covering both Hell's Gate and the Lake Naivasha boat safari.",
        "booking",
        521
    ),

    # 8. Fishing Tours
    (
        "What fish can we catch on a Lake Naivasha fishing tour?",
        "<p>Anglers typically catch <strong>Nile Tilapia, Largemouth Bass, and Black Bass</strong>. Tilapia is plentiful and delicious, while Largemouth Bass provides thrilling sport fishing in the papyrus channel margins.</p>",
        "You can catch Nile Tilapia, Largemouth Bass, and Black Bass on Lake Naivasha.",
        "wildlife",
        522
    ),
    (
        "Do we need to bring our own rods for a fishing charter?",
        "<p>Rafiki provides standard spinning rods, reels, and bait as part of our fishing tour package. However, if you are a passionate angler who prefers fly-fishing or specialist lures, you are welcome to bring your own gear.</p>",
        "No, we provide standard rods, reels, and bait, but serious anglers are welcome to bring their own gear.",
        "preparation",
        523
    ),
    (
        "Can we cook the fish we catch during the fishing tour?",
        "<p><strong>Yes!</strong> Any tilapia you catch can be taken to the Karagita Beach fish kitchens, where local chefs will clean, deep-fry, or charcoal-grill your catch on the spot and serve it with fresh ugali.</p>",
        "Yes, you can have your fresh catch cooked and served with ugali at the Karagita Beach fish kitchens.",
        "amenities",
        524
    ),

    # 9. Oloidien Bay
    (
        "Why should we visit Oloidien Bay instead of the main lake?",
        "<p>Oloidien Bay is slightly more alkaline and shallow, making it a distinct ecological zone. It is famous for hosting migratory Lesser Flamingos, dense hippo nursery pods, and unique waterbirds not found on the main lake.</p>",
        "Oloidien Bay is a quieter, slightly alkaline bay famous for flamingos, hippo nursery pods, and rare waterbirds.",
        "destination",
        525
    ),
    (
        "Are flamingos always visible in Oloidien Bay?",
        "<p>Flamingo presence is seasonal and depends heavily on the water level and alkalinity. They are most common between December and March, but we advise checking with our captains for real-time sightings before booking.</p>",
        "Flamingos are seasonal and depend on water conditions. We recommend checking with our captains for current status.",
        "wildlife",
        526
    ),
    (
        "How long does a boat safari to Oloidien Bay take?",
        "<p>Reaching Oloidien Bay requires passing through a scenic papyrus channel. We recommend a <strong>2-hour or 3-hour 'Full Lake Circuit' private charter</strong> to comfortably explore the bay and return to the main beach.</p>",
        "Exploring Oloidien Bay takes about 2 to 3 hours as part of our comprehensive Full Lake Circuit safari.",
        "timing",
        527
    ),

    # 10. Hippo Point Area
    (
        "Where is Hippo Point Naivasha located and how do we get there?",
        "<p>Hippo Point is situated on the southwestern shore of Lake Naivasha along South Lake Road. You can reach it via a scenic 30-minute drive from Naivasha Town, or by booking a direct 2-hour boat safari from Karagita Beach.</p>",
        "Hippo Point is on the southwest shore along South Lake Road, accessible via a 30-minute drive or a 2-hour boat safari.",
        "location",
        528
    ),
    (
        "Can we see the Hippo Point Tower from the boat safari?",
        "<p><strong>Yes!</strong> The iconic 17-meter-tall Victorian-style Hippo Point Tower rises beautifully above the acacia canopy and is clearly visible from our safari boats as we cruise the Hippo Point shoreline.</p>",
        "Yes, the 17-meter-tall Hippo Point Tower is clearly visible from the water as you cruise the shoreline.",
        "destination",
        529
    ),
    (
        "Is Hippo Point the best place on the lake to see baby hippos?",
        "<p><strong>Yes.</strong> The shallow, calm, papyrus-shielded waters of Hippo Point and adjacent Oloidien Bay serve as the lake's primary hippo nurseries, making it the absolute best area to spot mothers with small calves.</p>",
        "Yes, Hippo Point is the primary hippo nursery area on the lake and the best spot to see mothers with small calves.",
        "wildlife",
        530
    ),
]

print("=" * 60)
print("PHASE 10: NEW FAQs SEEDER")
print("=" * 60)

print("\n--- Injecting/Updating 30 Phase 10 FAQs ---")
created_count = 0
updated_count = 0
for q, a, plain, intent, order in faqs:
    dupes = FAQ.objects.filter(question=q)
    if dupes.count() > 1:
        keep = dupes.order_by('-id').first()
        dupes.exclude(id=keep.id).delete()
    faq, created = FAQ.objects.update_or_create(
        question=q,
        defaults={
            'answer': a,
            'plain_answer': plain,
            'search_intent': intent,
            'order': order,
            'is_active': True,
            'allow_indexing': True
        }
    )
    action = "NEW" if created else "UPD"
    print(f"  [{action}] {faq.question}")
    if created:
        created_count += 1
    else:
        updated_count += 1

print(f"\n{'=' * 60}")
print(f"PHASE 10 COMPLETE!")
print(f"  FAQs Created: {created_count}")
print(f"  FAQs Updated: {updated_count}")
print(f"  Total FAQs in DB: {FAQ.objects.filter(is_active=True).count()}")
print(f"{'=' * 60}")
