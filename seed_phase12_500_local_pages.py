"""
Phase 12: Seeding to exactly 1,000 total Local Pages in the database.
Deletes all previously generated duplicate/suffixed pages.
Uses 8 location-based templates and 140 unique Kenyan locations to generate
967 unique, non-duplicating local pages (no numbered suffixes).
Run: .venv\\Scripts\\python.exe seed_phase12_1000_local_pages.py
"""
import os, sys, django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import LocalPage

print("=" * 60)
print("PHASE 12: BULK UNIQUE LOCAL PAGES SEEDER (TARGET: 1,000 TOTAL)")
print("=" * 60)

# List of 33 original high-quality manual/phase 9 slugs to preserve
original_slugs = {
    'bird-watching-lake-naivasha',
    'birthday-boat-ride-lake-naivasha-party-safari',
    'boat-ride-at-lake-naivasha',
    'boat-ride-in-lake-naivasha',
    'boat-ride-on-lake-naivasha',
    'boat-rides-naivasha',
    'boat-safari-lake-naivasha',
    'crescent-island-tours',
    'crescent-island-walking-safari',
    'elsamere-conservation-centre',
    'hells-gate-lake-naivasha-boat-ride-combo',
    'hippo-point-naivasha',
    'hippo-point-naivasha-boat-safari',
    'jkia-nairobi-airport-to-lake-naivasha-transfer',
    'karagita-public-beach',
    'lake-naivasha-beach',
    'lake-naivasha-boat-ride-with-kids',
    'lake-naivasha-corporate-team-building',
    'lake-naivasha-fishing-tour',
    'lake-naivasha-photography-tour',
    'lake-naivasha-safari-boat-ride',
    'mombasa-to-lake-naivasha-train-flight-guide',
    'nairobi-to-lake-naivasha-drive-matatu-guide',
    'naivasha-tour-packages',
    'nakuru-to-lake-naivasha-drive-safari',
    'oloidien-bay-lake-naivasha',
    'private-boat-hire-lake-naivasha',
    'romantic-boat-ride-lake-naivasha-honeymoon',
    'sanctuary-farm-lake-naivasha',
    'sunset-cruises-naivasha',
    'test-image-page',
    'maasai-mara-to-lake-naivasha-drive',
    'tour-lake-naivasha'
}

# Delete any existing active local pages that are not part of the original 33
print("Cleaning up old generated duplicate/suffixed pages...")
all_active = LocalPage.objects.filter(is_active=True)
deleted_count = 0
for page in all_active:
    if page.slug not in original_slugs:
        page.delete()
        deleted_count += 1

print(f"Deleted {deleted_count} duplicate/temporary local pages.")

current_count = LocalPage.objects.filter(is_active=True).count()
print(f"Current preserved Local Pages: {current_count}")
needed = 1000 - current_count
print(f"Local Pages needed to reach 1,000: {needed}")

if needed <= 0:
    print("Already have 1,000+ Local Pages. Exiting.")
    sys.exit(0)

# =====================================================================
# 140 UNIQUE KENYAN LOCATIONS (Cities, Towns, Estates, Suburbs)
# =====================================================================
locations = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Ruiru", "Kikuyu", "Thika", "Garissa",
    "Ngong", "Karuri", "Naivasha", "Kitui", "Kiambu", "Kakamega", "Eldama Ravine", "Nyeri", "Meru", "Lodwar",
    "Athiriver", "Kitengela", "Rongai", "Syokimau", "Mlolongo", "Westlands", "Karen", "Runda", "Lavington", "Kilimani",
    "Kileleshwa", "Langata", "South C", "South B", "Embakasi", "Utawala", "Ruai", "Gigiri", "Muthaiga", "Pangani",
    "Ngara", "Parklands", "Eastleigh", "Kasarani", "Roysambu", "Kahawa Sukari", "Kahawa Wendani", "Juja", "Githurai",
    "Limuru", "Tigoni", "Kabete", "Uthiru", "Kinoo", "Muguga", "Wangige", "Banana", "Gilgil", "Mai Mahiu", "Nyahururu",
    "Nanyuki", "Karatina", "Othaya", "Mukurweini", "Kerugoya", "Kutus", "Chuka", "Embu", "Maua", "Isiolo", "Marsabit",
    "Maralal", "Subukia", "Molo", "Njoro", "Elburgon", "Solai", "Bahati", "Lanet", "Elementaita", "Ol Kalou",
    "Njabini", "Kinangop", "Narok", "Kilgoris", "Kericho", "Bomet", "Sotik", "Kisii", "Nyamira", "Oyugis", "Homa Bay",
    "Migori", "Kehancha", "Awendo", "Rongo", "Maseno", "Ahero", "Muhoroni", "Mumias", "Butere", "Bungoma", "Webuye",
    "Kimilili", "Malaba", "Busia", "Kitale", "Kapenguria", "Iten", "Kabarnet", "Kapsabet", "Voi", "Wundanyi", "Mwatate",
    "Taveta", "Malindi", "Kilifi", "Watamu", "Mtwapa", "Mariakani", "Diani", "Ukunda", "Msambweni", "Lamu", "Wajir",
    "Mandera", "Machakos", "Athi River", "Tala", "Kangundo", "Wote", "Kitengela Town", "Ongata Rongai", "Kajiado Town"
]

# =====================================================================
# 8 DIVERSE LOCATION-SPECIFIC PAGE TEMPLATES
# =====================================================================
topics = [
    {
        'title_tpl': "Lake Naivasha Boat Ride Price per Person from {item}",
        'seo_title_tpl': "Lake Naivasha Boat Ride Price per Person from {item} (2026)",
        'meta_description_tpl': "What is the Lake Naivasha boat ride price per person from {item}? Transparent pricing, group rates, and direct flat-rate charters. Book with Rafiki.",
        'kw_tpl': "Lake Naivasha boat ride price per person {item}",
        'content_tpl': """
<h2>Lake Naivasha Boat Ride Price: Direct from {item}</h2>
<p>Travelers from <strong>{item}</strong> asking <em>"What is the Lake Naivasha boat ride price per person?"</em> will find Rafiki's pricing to be the most transparent and competitive on the lake.</p>

<h3>Standard Pricing Structure</h3>
<ul>
    <li><strong>Shared Group Tour (per person):</strong> Budget-friendly rates for individuals and couples joining small groups.</li>
    <li><strong>Private Boat Charter (flat-rate per boat):</strong> Exclusive use of the vessel and captain. Ideal for families of 3+ from {item} as the cost divides favorably.</li>
    <li><strong>Luxury Pontoon Charter:</strong> For corporate groups and large family events requiring more deck space and stability.</li>
</ul>

<h3>No Hidden Fees from {item}</h3>
<p>Rafiki operates exclusively on direct, broker-free bookings. When you contact us from <strong>{item}</strong> via WhatsApp (<strong>+254 729 280 380</strong>), you receive the direct operator price with no shoreline broker commissions or hidden handling fees.</p>

<h3>Is There a Lake Naivasha Entry Fee?</h3>
<p><strong>No.</strong> Lake Naivasha does not have a mandatory public entry fee. You pay only for your boat charter. Crescent Island has a separate sanctuary entry fee paid on arrival.</p>
"""
    },
    {
        'title_tpl': "Best Boat Rides Naivasha near {item}",
        'seo_title_tpl': "Best Boat Rides Naivasha near {item} | 5-Star Rafiki Safaris",
        'meta_description_tpl': "Find the best boat rides in Naivasha near {item}. Premium hippo safaris, Crescent Island transfers, and sunset cruises. friendly Rafiki Boat Rides.",
        'kw_tpl': "best boat rides naivasha near {item}",
        'content_tpl': """
<h2>The #1 Rated Boat Ride Experience near {item}</h2>
<p>If you are looking for the <strong>best boat rides in Naivasha</strong> convenient to <strong>{item}</strong>, Rafiki is consistently Kenya's highest-rated freshwater safari operator. Our guest-first reputation reflects deep local experience of delivering extraordinary wildlife encounters on Lake Naivasha's papyrus-fringed waters.</p>

<h3>Why Rafiki Leads Near {item}</h3>
<p>Unlike generic speedboat operators, Rafiki provides certified life jackets for all ages, professionally trained naturalist-captain guides, and low-emission four-stroke engines that preserve the lake's quiet acoustic environment for optimal wildlife encounters.</p>

<h3>Our Most Popular Experiences</h3>
<ul>
    <li><strong>Hippo Pod Safari (1 hour):</strong> Close encounters with 30+ resident hippo pods.</li>
    <li><strong>Crescent Island Walking Safari Combo (2-3 hours):</strong> Boat transfer + walking among giraffes and zebras.</li>
    <li><strong>Golden Hour Sunset Cruise (1.5-2 hours):</strong> Mau Escarpment silhouettes and dramatic hippo activity at dusk.</li>
</ul>
<p>Book directly from <strong>{item}</strong> via WhatsApp: <strong>+254 729 280 380</strong></p>
"""
    },
    {
        'title_tpl': "Pontoon Boat Rides Naivasha for Groups from {item}",
        'seo_title_tpl': "Pontoon Boat Rides Naivasha near {item} | Group & Event Charters",
        'meta_description_tpl': "Book luxury pontoon boat rides in Naivasha for groups from {item}. Corporate events, birthdays, family reunions — flat-rate, full-deck charters with Rafiki.",
        'kw_tpl': "pontoon boat rides naivasha {item}",
        'content_tpl': """
<h2>Luxury Pontoon Charters on Lake Naivasha</h2>
<p>For groups of 8 or more traveling from <strong>{item}</strong>, Rafiki's spacious pontoon boat charters offer a premium, stable, and highly social wildlife experience unlike anything available on standard speedboats.</p>

<h3>The Pontoon Advantage</h3>
<ul>
    <li><strong>Wide flat deck</strong> — room to move, interact, and photograph freely.</li>
    <li><strong>Circular seating</strong> — ideal for corporate team discussions and group activities.</li>
    <li><strong>Full canvas shade cover</strong> — protection from Kenya's equatorial sun.</li>
    <li><strong>Zero rocking</strong> — perfect for passengers sensitive to motion or with mobility considerations.</li>
</ul>

<h3>Events We Cater For from {item}</h3>
<p>Pontoon safaris are our most popular option for: corporate team building retreats, birthday party celebrations, family reunion outings, anniversary cruises, and school educational trips. All events can be fully customized with our events coordination team.</p>
<p>Contact us from <strong>{item}</strong> at WhatsApp: <strong>+254 729 280 380</strong> to get a group quote.</p>
"""
    },
    {
        'title_tpl': "Crescent Island Boat Ride and Walking Safari near {item}",
        'seo_title_tpl': "Crescent Island Boat Ride near {item} | Walk with Giraffes",
        'meta_description_tpl': "Book a Crescent Island boat ride and walking safari near {item}. Walk among free-roaming giraffes and zebras in Kenya's most unique predator-free sanctuary.",
        'kw_tpl': "Crescent Island boat ride near {item}",
        'content_tpl': """
<h2>Walk Freely Among Wild Animals: Crescent Island Sanctuary</h2>
<p>For visitors from <strong>{item}</strong>, the Crescent Island walking safari is consistently described as the most extraordinary wildlife experience in Kenya — more intimate than any game drive and more thrilling than any zoo. There are no fences, no vehicles, and no predators — just you, on foot, amongst genuinely wild African animals.</p>

<h3>The Animals You Will Encounter</h3>
<ul>
    <li><strong>Maasai Giraffe</strong> — Africa's tallest animal, allowing close approach on foot.</li>
    <li><strong>Common Zebra</strong> — Family herds grazing peacefully around walking visitors.</li>
    <li><strong>Common Eland, Waterbuck, Impala, Wildebeest</strong> — abundant resident populations.</li>
    <li><strong>Grey Crowned Crane, Yellow-billed Stork, African Spoonbill</strong> — waterbirds along the shoreline.</li>
</ul>

<h3>How to Access Crescent Island from {item}</h3>
<p>Crescent Island is accessible only by boat from Karagita Beach or your hotel's private jetty. Rafiki provides direct, flat-rate boat transfers specifically for Crescent Island visits, with the captain waiting at the dock while you complete your walking safari at your own pace.</p>
<p>Book your Crescent Island combo from <strong>{item}</strong>: WhatsApp <strong>+254 729 280 380</strong></p>
"""
    },
    {
        'title_tpl': "Lake Naivasha Boat Safari from {item}: Wildlife, Pricing & Tips",
        'seo_title_tpl': "Lake Naivasha Boat Safari from {item} | Rafiki Wildlife Guide",
        'meta_description_tpl': "Complete Lake Naivasha boat safari guide for visitors from {item}: hippos, birds, Crescent Island, pricing, best times, and how to book directly with Rafiki.",
        'kw_tpl': "lake naivasha boat safari {item}",
        'content_tpl': """
<h2>The Complete Lake Naivasha Boat Safari Guide for {item} Visitors</h2>
<p>Lake Naivasha's freshwater ecosystem — sustained by underground springs and the Malewa River — hosts one of East Africa's most accessible concentrations of megafauna and waterbirds. For visitors making the journey from <strong>{item}</strong>, here is everything you need to know to plan the perfect boat safari.</p>

<h3>Wildlife Highlights</h3>
<p>Within minutes of departing Karagita Beach, your Rafiki charter will position you alongside:</p>
<ul>
    <li><strong>Hippo pods</strong> of 15–40 individuals resting in shallow channels.</li>
    <li><strong>African Fish Eagles</strong> perched on dead acacia branches, launching spectacular fishing dives.</li>
    <li><strong>Malachite and Giant Kingfishers</strong> patrolling papyrus edges.</li>
    <li><strong>Great White Pelicans</strong> in V-formation above the southern islands.</li>
</ul>

<h3>Best Time to Go from {item}</h3>
<p>We recommend departing from <strong>{item}</strong> early enough to reach the lake by 7:00–8:00 AM for the optimal morning safari window. Late afternoon (4:00–5:30 PM) is ideal for sunset cruises and active hippo return from daytime wallowing grounds.</p>

<h3>Direct Booking from {item}</h3>
<p>Avoid shoreline brokers at Karagita Beach who inflate prices with commissions. Book directly with Rafiki at WhatsApp: <strong>+254 729 280 380</strong> before departing {item} to guarantee your preferred time slot.</p>
"""
    },
    {
        'title_tpl': "Lake Naivasha Boat Rides near {item}: Visitor Guide & Booking",
        'seo_title_tpl': "Lake Naivasha Boat Rides near {item} | Rafiki Direct Booking",
        'meta_description_tpl': "Planning Lake Naivasha boat rides from {item}? Full visitor guide: what's included, safety, wildlife, and how to book the best direct rates with 5-star Rafiki.",
        'kw_tpl': "lake naivasha boat rides near {item}",
        'content_tpl': """
<h2>Lake Naivasha Boat Rides: Your Complete Visitor Guide from {item}</h2>
<p>Lake Naivasha — the great freshwater gem of Kenya's Rift Valley — is perfectly positioned for a day trip or weekend escape from <strong>{item}</strong>. A Rafiki boat ride delivers extraordinary wildlife encounters in a safe, professional, and educational environment that consistently earns 5-star reviews.</p>

<h3>What's Included in Your Boat Ride?</h3>
<ul>
    <li>Certified life jacket for every passenger (all sizes including infants).</li>
    <li>Professional naturalist captain providing wildlife commentary throughout.</li>
    <li>Private, exclusive use of the charter boat (no shared strangers).</li>
    <li>Flexible route customization based on your group's interests.</li>
</ul>

<h3>Safety Information for {item} Visitors</h3>
<p>Rafiki operates with a zero-incident safety record across deep local experience. Our captains are trained in first aid and emergency procedures. We enforce strict wildlife approach protocols — maintaining minimum 50-meter buffers from hippo pods and refusing to operate in deteriorating weather conditions.</p>

<h3>How to Book from {item}</h3>
<p>WhatsApp: <strong>+254 729 280 380</strong> — message us with your preferred date, group size, and duration. We respond within 1 hour during business hours and confirm your booking instantly.</p>
"""
    },
    {
        'title_tpl': "Hippo Boat Safari Lake Naivasha near {item}: The Complete Experience",
        'seo_title_tpl': "Hippo Boat Safari Lake Naivasha near {item} | Close Encounters",
        'meta_description_tpl': "Experience a thrilling hippo boat safari on Lake Naivasha near {item}. Close-up encounters with massive hippo pods, fish eagles, and papyrus channels. Book Rafiki.",
        'kw_tpl': "hippo boat safari lake naivasha {item}",
        'content_tpl': """
<h2>The Hippo Boat Safari: Lake Naivasha's Signature Experience near {item}</h2>
<p>No East African wildlife experience quite prepares you for the visceral proximity of a <strong>Lake Naivasha hippo boat safari</strong>. For visitors from or near <strong>{item}</strong>, this is the activity that defines the lake and generates the most enthusiastic reviews from returning guests.</p>

<h3>Understanding Hippo Behavior for Better Encounters</h3>
<p>Hippos are fundamentally water-dwelling mammals that spend 16–18 hours submerged to protect their sensitive skin from UV radiation. Our captains position the boat at the optimal approach angles where surface-resting pod members are most visible — typically in the shallow papyrus channels on the lake's western margin.</p>
<p>Male hippos defending their pod territory will yawn dramatically — exposing 50cm-long ivory tusks — a behavior our experienced captains can reliably trigger safely through expert boat positioning.</p>

<h3>Rafiki's Hippo Safety Protocol near {item}</h3>
<p>We maintain a strict <strong>50-meter minimum buffer</strong> from all hippo pods. Our low-emission four-stroke engines operate quietly to minimize disturbance. Captains cut engine and drift silently when approaching pods for the most intimate, undisturbed viewing experience.</p>

<h3>Book Your Hippo Safari from {item}</h3>
<p>WhatsApp: <strong>+254 729 280 380</strong> — mention your group size and preferred date. Morning slots (7:00 AM – 10:00 AM) offer the best hippo surface activity. We confirm bookings within 1 hour.</p>
"""
    },
    {
        'title_tpl': "Sunset Cruise Lake Naivasha near {item}: Romantic & Group Options",
        'seo_title_tpl': "Sunset Cruise Lake Naivasha near {item} | Rafiki Evening Charters",
        'meta_description_tpl': "Book a sunset cruise on Lake Naivasha near {item}. Romantic private charters and group evening safaris with hippos, flamingos, and Mau Escarpment sunset views.",
        'kw_tpl': "sunset cruise lake naivasha {item}",
        'content_tpl': """
<h2>Lake Naivasha Sunset Cruises: The Most Beautiful Hour on the Lake</h2>
<p>The hour before sunset on Lake Naivasha near <strong>{item}</strong> is one of the most cinematically beautiful moments in all of Kenya. The Mau Escarpment turns a deep amber. Mount Longonot's volcanic silhouette etches against flaming orange skies. And the lake itself — utterly calm in the evening air — transforms into a perfect mirror of the sky above.</p>

<h3>What Happens During a Sunset Cruise?</h3>
<p>Hippos begin returning from their daytime basking grounds, creating waves of surfacing activity. Fish eagles deliver their haunting sunset calls across the quiet water. Flamingo flocks wheel overhead in perfect formations. Rafiki's captains navigate to the prime viewpoints for each of these spectacles in sequence as the light fades.</p>

<h3>Romantic Private Charter Options near {item}</h3>
<p>Our romantic sunset charter is booked as a fully private, exclusive experience — just your group and your captain. We can coordinate arrangements for sparkling wine on board and post-cruise dinner reservations at lakeside restaurants for guests from <strong>{item}</strong>.</p>

<h3>Group Sunset Safaris</h3>
<p>For corporate groups, family reunions, and birthday celebrations from <strong>{item}</strong>, our pontoon sunset charter provides a spacious, convivial floating venue as the lake turns golden. Book well in advance — weekend sunset slots sell out quickly.</p>
<p>WhatsApp: <strong>+254 729 280 380</strong></p>
"""
    },
]

# =====================================================================
# GENERATE PAGES COMBINATORIALLY (NO REPETITIVE SUFFIXES)
# =====================================================================
generated_pages = []
total_combinations = len(topics) * len(locations)

print(f"Combinatorial Pool Size: {len(topics)} templates * {len(locations)} locations = {total_combinations} unique combinations.")

# Generate pages in a distributed grid to maximize variety across locations and topics
idx = 0
while len(generated_pages) < needed and idx < total_combinations:
    # Use topic-major and location-minor loop mapping
    topic_idx = idx % len(topics)
    loc_idx = (idx // len(topics)) % len(locations)
    
    topic = topics[topic_idx]
    loc = locations[loc_idx]

    title = topic['title_tpl'].format(item=loc)
    slug = slugify(title)

    # Since we use deterministic unique location-topic pairs, collisions should only occur if
    # the page already exists in the original 33. In that case, we simply SKIP it completely.
    if any(p['slug'] == slug for p in generated_pages) or LocalPage.objects.filter(slug=slug).exists():
        idx += 1
        continue

    seo_title = topic['seo_title_tpl'].format(item=loc)[:70]
    meta_desc = topic['meta_description_tpl'].format(item=loc)[:160]
    kw = topic['kw_tpl'].format(item=loc)
    content = topic['content_tpl'].format(item=loc).strip()

    generated_pages.append({
        'title': title,
        'slug': slug,
        'seo_title': seo_title,
        'meta_description': meta_desc,
        'primary_keyword': kw,
        'location': loc,
        'modifiers': "price, reviews, boat ride, safari, hippo, pontoon",
        'content': content
    })
    idx += 1

print(f"Total new unique local pages compiled: {len(generated_pages)}")

# =====================================================================
# BULK INSERT INTO DATABASE
# =====================================================================
created_count = 0
for i, data in enumerate(generated_pages, 1):
    page, created = LocalPage.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'seo_title': data['seo_title'],
            'meta_description': data['meta_description'],
            'primary_keyword': data['primary_keyword'],
            'location': data['location'],
            'modifiers': data['modifiers'],
            'content': data['content'],
            'is_active': True,
            'allow_indexing': True
        }
    )
    if created:
        created_count += 1
    if i % 100 == 0:
        print(f"  Progress: {i}/{len(generated_pages)} pages processed...")

print(f"\n{'=' * 60}")
print(f"PHASE 12 COMPLETE!")
print(f"  Local Pages Created: {created_count}")
print(f"  Total Local Pages in Database: {LocalPage.objects.filter(is_active=True).count()}")
print(f"{'=' * 60}")
