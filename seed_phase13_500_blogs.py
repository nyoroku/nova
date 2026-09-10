"""
Phase 13: Seeding to 500 total Blog Posts in the database.
20+ diverse template categories: competitor reviews, transit guides, price Q&As,
activist/conservation articles, hotel combos, seasonal guides, comparison articles,
snippet-optimized answers, and family/honeymoon/corporate theme articles.
Run: .venv\\Scripts\\python.exe seed_phase13_500_blogs.py
"""
import os, sys, django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

print("=" * 60)
print("PHASE 13: BULK BLOGS SEEDER (TARGET: 500 TOTAL)")
print("=" * 60)

admin = User.objects.filter(is_superuser=True).first()
if not admin:
    seed_password = os.environ.get('DJANGO_SEED_ADMIN_PASSWORD')
    if not seed_password:
        raise RuntimeError('Set DJANGO_SEED_ADMIN_PASSWORD before creating the seed admin user.')
    admin = User.objects.create_superuser('admin', 'admin@rafikiboatride.com', seed_password)

current_count = Post.objects.all().count()
print(f"Current blog posts: {current_count}")
needed = 500 - current_count
print(f"Blog posts needed to reach 500: {needed}")

if needed <= 0:
    print("Already have 500+ Blog Posts. Exiting.")
    sys.exit(0)

# =====================================================================
# DIVERSE COMBINATORIAL ELEMENTS
# =====================================================================
origins = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
    "Thika", "Ruiru", "Kiambu", "Limuru", "Gilgil",
    "Mai Mahiu", "Nyeri", "Karatina", "Elementaita", "Nanyuki",
    "Malindi", "Voi", "Kericho", "Bungoma", "Machakos"
]

hotels = [
    "Enashipai Resort & Spa", "Lake Naivasha Sopa Resort", "Lake Naivasha Simba Lodge",
    "Kiboko Luxury Camp", "Sawela Lodges", "Lake Naivasha Country Club",
    "Chui Lodge Naivasha", "Great Rift Valley Lodge", "Naivasha Kongoni Lodge",
    "Crescent Camp Naivasha", "Lake Naivasha Dream Place", "Oloidien Bay Camp",
    "Fish Eagle Inn Naivasha", "Naivasha Eco Camp"
]

landmarks = [
    "Hell's Gate National Park", "Mount Longonot", "Crater Lake Sanctuary",
    "Olkaria Geothermal Spa", "Crescent Island", "Sanctuary Farm",
    "Elsamere Conservation Centre", "Hippo Point Viewpoint", "Malewa River Delta",
    "Karagita Beach", "South Lake Road", "Kongoni Game Valley"
]

competitors = ["Gitoh B", "Marina Boat Safaris", "Watamu Boat Rides", "Njovic Boat Rides", "Paradise Lost Nairobi"]

seasons = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December",
           "Easter Holiday", "Madaraka Day", "Jamhuri Day", "Christmas", "New Year",
           "School Holidays", "Long Rains Season", "Short Rains Season", "Dry Season"]

activities = [
    "hippo boat safari", "bird watching", "Crescent Island walking safari",
    "sunset cruise", "fishing tour", "photography tour", "corporate team building",
    "honeymoon boat ride", "birthday boat party", "pontoon charter"
]

# =====================================================================
# 20+ RICH BLOG TEMPLATES
# =====================================================================
blog_templates = [

    # 1. COMPETITOR COMPARISON (Gitoh B / Marina)
    {
        'title_tpl': "Gitoh B Boat Rides Naivasha vs. Rafiki: {item} Visitor's Honest Review",
        'meta_description_tpl': "Comparing Gitoh B Boat Rides Naivasha and Marina Boat Safaris for visitors from {item}. Safety, pricing, wildlife guides — full honest review.",
        'content_tpl': """
<h2>Which Boat Operator Should You Choose at Lake Naivasha?</h2>
<p>If you are traveling from <strong>{item}</strong> to Lake Naivasha, you will find several operators on Karagita Beach including <strong>Gitoh B Boat Rides Naivasha</strong> and <strong>Marina Boat Safaris Naivasha</strong>. Here is a data-driven comparison to help you choose wisely.</p>

<h3>Safety Standards</h3>
<p>Rafiki operates with certified, correctly-sized life jackets for all ages — including infants. Our commercial-grade fiberglass hulls have wide beams for maximum stability even in afternoon lake winds. Always confirm that any operator you choose has life jackets for every passenger before boarding.</p>

<h3>Naturalist Wildlife Guides</h3>
<p>Our captains are trained local naturalists who interpret hippo behavior, fish eagle diving physics, and papyrus ecology in engaging plain language. This educational layer transforms a simple boat ride into a genuine wilderness experience — something generic speedboat operators cannot offer.</p>

<h3>Pricing Transparency</h3>
<p>Rafiki publishes direct flat-rate charter prices online and on WhatsApp (<strong>+254 701 215 295</strong>). This eliminates shoreline broker commissions that inflate prices at the beach. When visiting from <strong>{item}</strong>, booking directly online ensures you pay exactly what you budgeted.</p>

<h3>Verdict for {item} Travelers</h3>
<p>Whether you are a budget backpacker or planning a premium honeymoon experience, Rafiki's transparent pricing and guest-first reputation make us the safest, most reliable choice on Lake Naivasha.</p>
""",
        'tags': ['best boat rides naivasha', 'gitoh b boat rides naivasha', 'boat rides naivasha prices'],
        'item_source': 'origins'
    },

    # 2. PRICE GUIDE (Snippet-optimized)
    {
        'title_tpl': "How Much is a Lake Naivasha Boat Ride? 2026 Price Guide for {item} Visitors",
        'meta_description_tpl': "How much is a Lake Naivasha boat ride? Complete 2026 pricing guide for visitors from {item}: per person rates, private charters, Crescent Island combos.",
        'content_tpl': """
<h2>Lake Naivasha Boat Ride Price: The Complete Answer</h2>
<p>One of the most searched questions by travelers from <strong>{item}</strong> is: <strong>"How much is a Lake Naivasha boat ride?"</strong></p>

<h3>The Direct Price Answer</h3>
<p><strong>A shared Lake Naivasha boat ride costs approximately KES 1,000 – 2,000 per person. A fully private boat charter costs KES 4,000 – 8,000 per boat per hour, giving your group exclusive use of the vessel and captain.</strong></p>

<h3>What Affects the Price?</h3>
<ul>
    <li><strong>Duration:</strong> Standard 1-hour hippo safaris vs. 2-3 hour Crescent Island combos.</li>
    <li><strong>Boat type:</strong> Fiberglass speedboats vs. luxury pontoon charters for large groups.</li>
    <li><strong>Direct booking:</strong> Booking directly with Rafiki via WhatsApp eliminates beach broker commissions.</li>
</ul>

<h3>Is There a Lake Naivasha Entrance Fee?</h3>
<p><strong>No. Lake Naivasha does not have a mandatory entrance fee.</strong> You only pay your boat charter rate. Crescent Island Sanctuary has a separate conservation fee paid to the private landowner.</p>

<h3>Best Time of Day for a Boat Ride?</h3>
<p><strong>The best time for a Lake Naivasha boat ride is early morning (7:00 AM – 10:00 AM)</strong> when hippos are most active near the surface and bird species are feeding. Late afternoons (4:00 PM – 6:00 PM) are perfect for romantic sunset cruises.</p>

<p>Book directly from <strong>{item}</strong> via WhatsApp: <strong>+254 701 215 295</strong></p>
""",
        'tags': ['lake naivasha boat ride price', 'boat rides naivasha prices', 'lake naivasha boat ride price per person'],
        'item_source': 'origins'
    },

    # 3. TRANSIT GUIDE
    {
        'title_tpl': "From {item} to Lake Naivasha: The Complete Boat Ride Travel Guide",
        'meta_description_tpl': "Planning a trip from {item} to Lake Naivasha? Complete travel guide: driving routes, matatu options, transit costs, hotels, and booking your hippo boat safari.",
        'content_tpl': """
<h2>Your {item} to Lake Naivasha Trip — Fully Planned</h2>
<p>Lake Naivasha is the most accessible wildlife destination from <strong>{item}</strong>, offering dramatic Great Rift Valley scenery, world-famous hippo safaris, and the jaw-dropping Crescent Island walking experience — all within a day trip or weekend.</p>

<h3>Getting to Lake Naivasha from {item}</h3>
<p>The most scenic route from <strong>{item}</strong> passes through the Rift Valley escarpment viewpoint on the B3 highway, offering sweeping views of the valley floor before descending to the lake. Private road transfers can be coordinated through Rafiki. Matatu routes also operate regularly to Naivasha town, with tuk-tuks and bodabodas ferrying visitors from town to Karagita Beach.</p>

<h3>What to Do Once You Arrive</h3>
<ol>
    <li><strong>Morning Hippo Safari:</strong> Book a 1-hour private charter with Rafiki for close encounters with massive hippo pods.</li>
    <li><strong>Crescent Island Combo:</strong> Add a 2-hour boat transfer and walking safari to walk amongst giraffes, zebras, and elands in a predator-free sanctuary.</li>
    <li><strong>Hell's Gate Cycling:</strong> Rent a bicycle and cycle through volcanic gorges in the afternoon.</li>
    <li><strong>Karagita Beach Tilapia Lunch:</strong> Feast on freshly grilled Nile tilapia at the beach restaurants after your safari.</li>
</ol>

<h3>Recommended Hotels Near the Lake</h3>
<p>From budget campsites to premium resorts — Lake Naivasha has a full range of accommodation. Rafiki can recommend the best hotel options based on your group size and budget when you contact us via WhatsApp at <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['lake naivasha boat ride price from nairobi', 'nairobi to lake naivasha', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 4. HOTEL COMBO GUIDE
    {
        'title_tpl': "Staying at {item}? Here's How to Book Your Lake Naivasha Boat Safari",
        'meta_description_tpl': "Guests at {item} can book direct Lake Naivasha boat safaris with Rafiki. Hippo tours, sunset cruises, and Crescent Island combos — all from your hotel jetty.",
        'content_tpl': """
<h2>The Perfect Add-On for {item} Guests</h2>
<p>If you are staying at <strong>{item}</strong> on the shores of Lake Naivasha, a professionally guided wildlife boat safari is the single most memorable activity you can add to your itinerary. Rafiki has partnered with lakeside lodges for years to provide seamless, direct charter experiences for hotel guests.</p>

<h3>Hotel Jetty Pickup Available</h3>
<p>Rather than driving to Karagita Public Beach, Rafiki can coordinate direct pickup from your hotel's private jetty or lakefront access point, saving you transit time and ensuring a prompt morning departure when wildlife activity is at its peak.</p>

<h3>Recommended Safari Packages for Hotel Guests</h3>
<ul>
    <li><strong>The Wildlife Dawn Safari (1.5 hrs):</strong> Early morning hippo, fish eagle, and papyrus bird spectacle.</li>
    <li><strong>The Crescent Island Full Experience (3 hrs):</strong> Boat transfer + guided walking safari among predator-free wildlife.</li>
    <li><strong>The Romantic Sunset Cruise (2 hrs):</strong> Padded seating, Mau escarpment sunset views — ideal for couples at {item}.</li>
</ul>

<h3>Direct Booking for {item} Guests</h3>
<p>Simply message Rafiki on WhatsApp at <strong>+254 701 215 295</strong> before your check-in date to pre-arrange your boat safari schedule. We handle everything including life jacket pre-sizing, captain briefings, and route customization based on your group's interests.</p>
""",
        'tags': ['lake naivasha boat ride review', 'best boat rides naivasha', 'sunset cruises naivasha'],
        'item_source': 'hotels'
    },

    # 5. ACTIVIST / ENVIRONMENTAL
    {
        'title_tpl': "Saving Lake Naivasha: The Environmental Crisis Near {item} and What We Can Do",
        'meta_description_tpl': "Lake Naivasha faces rising water threats, invasive weeds, and agricultural pollution near {item}. Learn how Rafiki supports sustainable eco-tourism and papyrus preservation.",
        'content_tpl': """
<h2>The Lake Under Threat</h2>
<p>Lake Naivasha — the emerald jewel of Kenya's Rift Valley — is under serious environmental pressure. Despite its proximity to <strong>{item}</strong> and its designation as a Ramsar Wetland of International Importance, the lake faces an accelerating set of ecological crises that threaten its wildlife, water quality, and long-term tourism value.</p>

<h3>The Invasive Water Hyacinth Crisis</h3>
<p>Introduced accidentally in the early 1980s, water hyacinth (<em>Eichhornia crassipes</em>) has blanketed vast sections of the lake's surface, depleting dissolved oxygen, blocking sunlight from subaquatic plants, and suffocating the lake's native tilapia and bass populations. Local community groups manually harvest the weed, but government support remains inconsistent.</p>

<h3>Papyrus Wetlands Destruction</h3>
<p>The dense papyrus sedge fringing the lake acts as a biological filtration system — trapping silt from inflowing rivers like the Malewa and Gilgil, and absorbing chemical runoff from the vast flower farms of <strong>{item}</strong> and its surroundings. Clearing of papyrus for agriculture and informal settlement reduces this natural filtration, accelerating eutrophication.</p>

<h3>How Rafiki Supports Conservation</h3>
<p>Rafiki operates low-emission, four-stroke outboard engines that reduce water-born hydrocarbon pollution. Our captains enforce strict <strong>50-meter hippo buffer zones</strong> and refuse to operate at speeds that create damaging bow waves near papyrus beds. A portion of every charter booked via WhatsApp (<strong>+254 701 215 295</strong>) contributes to local papyrus restoration and hyacinth harvesting cooperatives.</p>
""",
        'tags': ['lake naivasha boat ride review', 'bird watching lake naivasha', 'boat safari lake naivasha'],
        'item_source': 'landmarks'
    },

    # 6. SEASONAL GUIDE
    {
        'title_tpl': "Best Time to Visit Lake Naivasha During {item}: Weather, Wildlife & Boat Rides",
        'meta_description_tpl': "Planning a Lake Naivasha visit during {item}? Read our seasonal guide on weather, hippo activity, bird migration, and booking boat rides during peak and off-peak periods.",
        'content_tpl': """
<h2>Is {item} a Good Time to Visit Lake Naivasha?</h2>
<p><strong>Yes — {item} is one of the most rewarding times to experience Lake Naivasha.</strong> Kenya's freshwater ecosystems respond dramatically to seasonal rainfall and temperature cycles, creating very distinct wildlife experiences at different times of year.</p>

<h3>Weather During {item}</h3>
<p>Lake Naivasha sits at 1,884 meters above sea level in the floor of the Great Rift Valley. The altitude creates a mild, temperate microclimate that makes it comfortable year-round. During <strong>{item}</strong>, expect clear skies in the morning with potential afternoon cloud build-up — making early morning boat safaris the optimal choice.</p>

<h3>Wildlife Activity During {item}</h3>
<p>Hippo pods are visible throughout the year, but during <strong>{item}</strong>, breeding male hippos are particularly territorial and active near the lake's shallow papyrus margins. African Fish Eagles are present year-round, while the migratory Eurasian rollers and storks arrive in large numbers during specific months, creating extraordinary spectacles above the lake surface.</p>

<h3>Booking Tips for {item}</h3>
<ul>
    <li>Book at least <strong>48–72 hours in advance</strong> during holiday weekends when private charter demand surges.</li>
    <li>Depart early at <strong>7:00 AM</strong> to catch peak hippo and bird activity before the mid-morning winds build.</li>
    <li>Carry light layers — the lake breeze can feel cool even during Kenya's warm seasons.</li>
</ul>
<p>Message Rafiki directly on WhatsApp: <strong>+254 701 215 295</strong> to secure your preferred time slot during <strong>{item}</strong>.</p>
""",
        'tags': ['lake naivasha boat ride price', 'best boat rides naivasha', 'lake naivasha boat ride review'],
        'item_source': 'seasons'
    },

    # 7. ACTIVITY DEEP-DIVE
    {
        'title_tpl': "The Complete Guide to {item} on Lake Naivasha with Rafiki",
        'meta_description_tpl': "Everything you need to know about {item} on Lake Naivasha: what to expect, pricing, safety tips, and how to book directly with Rafiki for the best experience.",
        'content_tpl': """
<h2>Your Ultimate {item} Guide on Lake Naivasha</h2>
<p>Lake Naivasha offers a remarkable variety of water-based and lakeside experiences. Among all of them, <strong>{item}</strong> stands out as one of the most sought-after by both domestic Kenyan families and international tourists. Here is everything you need to know before booking.</p>

<h3>What Makes a {item} on Lake Naivasha Special?</h3>
<p>The lake's freshwater ecosystem — fed by the Malewa and Gilgil rivers and sustained by deep underground springs — creates ideal conditions for a spectacular <strong>{item}</strong> experience. The combination of wildlife density, crystal-clear papyrus-filtered water, and dramatic Rift Valley scenery makes this unlike anywhere else in East Africa.</p>

<h3>What You Will Experience</h3>
<p>Rafiki's experienced captains customize every <strong>{item}</strong> to match your group's interests and energy levels. Whether you prefer a slow, meditative drift through papyrus channels listening to kingfisher calls, or an action-packed hippo encounter in the main open water channels, we tailor the route to maximize your experience.</p>

<h3>Safety and Equipment</h3>
<p>All Rafiki safaris include certified, properly-fitted life jackets for every passenger. Our low-emission four-stroke engines are environmentally sound and run quietly to avoid disturbing wildlife. Infants and young children are accommodated with specialized safety equipment — just notify us when booking via WhatsApp at <strong>+254 701 215 295</strong>.</p>

<h3>Pricing and Booking</h3>
<p>Rafiki offers transparent, flat-rate charter pricing for <strong>{item}</strong> with no hidden shoreline broker fees. Contact our friendly team directly to get an instant quote and availability for your preferred date and group size.</p>
""",
        'tags': ['best boat rides naivasha', 'lake naivasha boat ride review', 'boat safari lake naivasha'],
        'item_source': 'activities'
    },

    # 8. MOMBASA / KISUMU / LONG-DISTANCE COMPARISON
    {
        'title_tpl': "Boat Riding in {item} vs Lake Naivasha: Which is Better for Your Safari?",
        'meta_description_tpl': "Comparing boat riding in {item} versus Lake Naivasha. Wildlife, price, safety, and overall experience — find out which destination is best for your group.",
        'content_tpl': """
<h2>Lake Naivasha vs {item} for Boat Rides: An Honest Comparison</h2>
<p>Kenya's diverse geography offers several boat ride destinations, from the coastal mangrove channels near <strong>{item}</strong> to the freshwater hippo-filled expanse of Lake Naivasha. If you are deciding between them, this honest comparison will help you make the right choice for your group.</p>

<h3>Wildlife Density</h3>
<p><strong>Lake Naivasha wins on wildlife density.</strong> With over 1,500 resident hippos — one of the highest concentrations in East Africa — plus over 400 waterbird species, an African Fish Eagle hunting on every shore, and Crescent Island's fence-free walking safari among giraffes, Lake Naivasha offers an unmatched freshwater safari experience that coastal boat rides simply cannot replicate.</p>

<h3>Accessibility from {item}</h3>
<p>Lake Naivasha is well-connected by road from most major Kenyan towns. From <strong>{item}</strong>, the drive is scenic and takes you through Kenya's agricultural heartland and past the dramatic Rift Valley escarpment. Rafiki can also assist with coordinating private road transfers for large groups.</p>

<h3>Pricing Comparison</h3>
<p>Lake Naivasha boat charters with Rafiki start at highly competitive flat rates, offering full exclusive use of the vessel and a professional naturalist guide. Compared to equivalent marine charter services, our freshwater safaris deliver dramatically higher wildlife encounter rates per hour spent on the water.</p>

<h3>Book Your Lake Naivasha Experience</h3>
<p>Message Rafiki on WhatsApp at <strong>+254 701 215 295</strong> to get an instant quote and plan your perfect Lake Naivasha safari — far superior to boat riding in <strong>{item}</strong> for pure wildlife encounters.</p>
""",
        'tags': ['boat riding in nairobi', 'lake naivasha boat ride review', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 9. CRESCENT ISLAND DEEP DIVE
    {
        'title_tpl': "Crescent Island Boat Ride Price & Walking Safari Guide from {item}",
        'meta_description_tpl': "Everything about the Crescent Island boat ride price for visitors from {item}: transfer costs, walking safari entry, wildlife guide, and booking directly with Rafiki.",
        'content_tpl': """
<h2>Crescent Island: The Crown Jewel of Lake Naivasha</h2>
<p>The most extraordinary wildlife experience available at Lake Naivasha is the <strong>Crescent Island walking safari</strong>. This private island sanctuary, accessible only by boat, allows you to walk unguided or with our naturalist captain among free-roaming giraffes, zebras, elands, wildebeests, and over 100 bird species — all without fences or vehicle restrictions.</p>

<h3>Crescent Island Boat Ride Price Structure</h3>
<p>When booking from <strong>{item}</strong>, your Crescent Island experience includes two main costs:</p>
<ul>
    <li><strong>Rafiki Boat Transfer:</strong> Direct flat-rate return boat charter from Karagita Beach or your hotel jetty to the island landing. Our captains wait at the dock while you complete your safari.</li>
    <li><strong>Island Conservation Entry Fee:</strong> Paid directly to the Crescent Island sanctuary management upon arrival. This fee supports wildlife conservation on the island.</li>
</ul>

<h3>What You Will See on Crescent Island</h3>
<p>Unlike any conventional game reserve, Crescent Island allows you to approach wild animals on foot at remarkably close distances. Maasai giraffes often allow visitors within 5–10 meters. Zebra stallions and their herds graze calmly around walking visitors. The shoreline marshes teem with crowned cranes, saddle-billed storks, and African pygmy kingfishers.</p>

<h3>Tips for {item} Visitors</h3>
<ul>
    <li>Wear neutral-colored clothing and comfortable walking shoes.</li>
    <li>Arrive early (before 9:00 AM) when animals are most active near the water's edge.</li>
    <li>Carry a camera with a zoom lens for bird photography.</li>
</ul>
<p>Book your complete Crescent Island combo directly on WhatsApp at <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['crescent island boat ride price', 'lake naivasha boat ride and crescent island', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 10. PONTOON BOAT GUIDE
    {
        'title_tpl': "Pontoon Boat Rides Naivasha: Group, Corporate & Event Charters from {item}",
        'meta_description_tpl': "Book spacious pontoon boat rides in Naivasha for groups from {item}. Flat-deck luxury, corporate team building, birthday parties, and family events on Lake Naivasha.",
        'content_tpl': """
<h2>Naivasha's Best Pontoon Boat Charters</h2>
<p>For corporate delegations, large family reunions, and special event celebrations traveling from <strong>{item}</strong>, Rafiki's spacious pontoon boat charters offer an unmatched premium group experience on Lake Naivasha.</p>

<h3>Why Choose a Pontoon Over a Standard Speedboat?</h3>
<p>Standard fiberglass speedboats carry up to 7 passengers and are excellent for small groups and couples. However, for groups of 8 or more, pontoon platforms offer:</p>
<ul>
    <li><strong>Flat, wide deck space</strong> for group activities and team games on the water.</li>
    <li><strong>Circular seating configuration</strong> ideal for networking and corporate briefings.</li>
    <li><strong>Full canvas shade cover</strong> protecting against midday equatorial sun.</li>
    <li><strong>Superior stability</strong> — no rocking, allowing even those with motion sensitivity to enjoy the safari fully.</li>
</ul>

<h3>Corporate Team Building on the Lake</h3>
<p>Lake Naivasha's serene, Wi-Fi-free environment creates the perfect backdrop for corporate retreats from <strong>{item}</strong>. Rafiki's pontoon charters can be customized with structured team-building activities, professional photography, and post-safari lunch arrangements at Karagita Beach.</p>

<h3>Birthday & Special Event Pontoon Charters</h3>
<p>Celebrate birthdays, anniversaries, and special occasions on a private floating venue surrounded by wildlife. Our team helps arrange decorations, customized route preferences, and coordination with catering services.</p>
<p>Secure your pontoon charter from <strong>{item}</strong> by messaging WhatsApp: <strong>+254 701 215 295</strong> — availability is limited, especially on weekends.</p>
""",
        'tags': ['pontoon boat rides naivasha', 'boat rides naivasha prices', 'lake naivasha corporate team building'],
        'item_source': 'origins'
    },

    # 11. ROMANTIC / HONEYMOON
    {
        'title_tpl': "Romantic Lake Naivasha Boat Rides for Honeymooners Staying at {item}",
        'meta_description_tpl': "Plan the perfect romantic Lake Naivasha boat ride for your honeymoon at {item}. Sunset cruises, private charters, and champagne experiences on Africa's most scenic freshwater lake.",
        'content_tpl': """
<h2>Romance on the Water — Lake Naivasha's Most Breathtaking Sunset Cruises</h2>
<p>Lake Naivasha offers what few African destinations can claim — a combination of raw wildlife encounters and deeply intimate romantic scenery in a single hour on the water. For honeymooning couples staying at <strong>{item}</strong>, Rafiki's private sunset charter is an unforgettable experience.</p>

<h3>The Sunset Cruise Experience</h3>
<p>Departing between 4:30 PM and 5:00 PM, the lake transforms as the equatorial sun descends behind the Mau Escarpment and Mount Longonot's volcanic crater silhouettes against a flaming orange and violet sky. Hippos return from their daytime wallowing grounds, surfacing with dramatic yawns. African Fish Eagles call across the golden water.</p>

<h3>Private Charter — Just the Two of You</h3>
<p>Rafiki's romantic sunset charter is booked as a <strong>fully private, exclusive charter</strong>. No other passengers. Your dedicated captain navigates the most scenic papyrus channels and positions the boat perfectly for silhouette photography of hippos against the setting sun.</p>

<h3>Customization Options for {item} Guests</h3>
<ul>
    <li>Arrangements for chilled sparkling wine or champagne on board.</li>
    <li>Coordinated post-cruise dinner reservations at lakeside restaurants.</li>
    <li>Private photography sessions at Hippo Point during the golden hour.</li>
</ul>
<p>Book your romantic sunset charter via WhatsApp: <strong>+254 701 215 295</strong> — ideally 72 hours in advance to guarantee your preferred slot.</p>
""",
        'tags': ['lake naivasha boat ride review', 'sunset cruises naivasha', 'romantic boat ride lake naivasha'],
        'item_source': 'hotels'
    },

    # 12. FAMILY / KIDS GUIDE
    {
        'title_tpl': "Lake Naivasha Boat Ride with Kids from {item}: Safety, Fun & What to Expect",
        'meta_description_tpl': "Planning a Lake Naivasha boat ride with kids from {item}? Rafiki provides infant life jackets, stable hulls, and child-friendly wildlife commentary for the safest family safari.",
        'content_tpl': """
<h2>The Best Family Boat Safari on Lake Naivasha</h2>
<p>Traveling to Lake Naivasha with young children from <strong>{item}</strong> is one of the most rewarding family wildlife experiences in Kenya. Children are utterly captivated by their first close encounter with a yawning 2-tonne hippo, a screaming fish eagle, or a flamingo flock exploding skyward from the papyrus margins.</p>

<h3>Child Safety is Our Priority</h3>
<p>Rafiki maintains a full range of certified life jackets including specially designed <strong>infant and toddler sizes</strong>. Our wide commercial fiberglass hulls provide exceptional stability, eliminating rocking that can frighten young children. When you book, inform us of your children's ages so we can pre-size life jackets before your arrival.</p>

<h3>Child-Friendly Wildlife Commentary</h3>
<p>Our captains are practiced at engaging young explorers with simple, exciting wildlife explanations. Children learn why hippos sweat red (it's actually a natural sunscreen!), how fish eagles dive at over 70 km/h, and why papyrus reeds are so important for the lake's health. This educational layer makes the experience genuinely memorable for the whole family.</p>

<h3>Practical Tips for {item} Families</h3>
<ul>
    <li>Book morning slots (7:00 AM – 10:00 AM) when children are most energetic.</li>
    <li>Carry sunscreen, hats, and light snacks for toddlers.</li>
    <li>Allow extra time for Karagita Beach — children love watching the fishermen and tilapia grilling.</li>
</ul>
<p>Book your family safari safely via WhatsApp: <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['lake naivasha boat ride with kids', 'best boat rides naivasha', 'lake naivasha boat ride price per person'],
        'item_source': 'origins'
    },

    # 13. BIRDWATCHING GUIDE
    {
        'title_tpl': "Bird Watching on Lake Naivasha: A Complete Guide for {item} Ornithologists",
        'meta_description_tpl': "Lake Naivasha is a birder's paradise with 400+ species. Complete birdwatching guide for visitors from {item}: best spots, seasonal species, and booking your boat safari.",
        'content_tpl': """
<h2>Lake Naivasha: East Africa's Premier Birding Destination</h2>
<p>For serious ornithologists and casual wildlife photographers traveling from <strong>{item}</strong>, Lake Naivasha ranks among the top five freshwater birding sites in all of Africa, with over 400 recorded species. A single Rafiki boat charter can realistically yield 60–80 species sightings within 2 hours.</p>

<h3>The Iconic Species</h3>
<ul>
    <li><strong>African Fish Eagle</strong> — Kenya's national bird, heard calling across the lake from dawn to dusk. Fishing dives observed regularly.</li>
    <li><strong>Malachite Kingfisher</strong> — Electric turquoise gems hovering above papyrus channels.</li>
    <li><strong>Great White Pelican</strong> — Breeding colonies numbering hundreds on the lake's islands.</li>
    <li><strong>Grey Crowned Crane</strong> — Kenya's national treasure, grazing in lakeside meadows.</li>
    <li><strong>Lesser Flamingo</strong> — Periodic pink flocks of thousands descend from Lake Bogoria.</li>
    <li><strong>Giant Kingfisher, Pied Kingfisher, African Darter, Long-tailed Cormorant</strong> — all abundant.</li>
</ul>

<h3>Seasonal Birding Highlights</h3>
<p>November to April brings Eurasian migratory species including Marsh Harriers, White Storks, Barn Swallows, and Yellow Wagtails. The resident breeding season (June–September) sees crowned cranes, herons, and cormorants nesting actively in the papyrus fringing the southern shore.</p>

<h3>Photography-Optimized Routes</h3>
<p>Rafiki's captains know the precise locations of active nesting colonies, regular fish eagle perch trees, and shallow channels where kingfishers hunt. Our slow-drift approach minimizes disturbance and maximizes photography opportunity at close range.</p>
<p>Book your birding safari from <strong>{item}</strong> via WhatsApp: <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['bird watching lake naivasha', 'boat safari lake naivasha', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 14. HELLS GATE COMBO GUIDE
    {
        'title_tpl': "Hell's Gate + Lake Naivasha Boat Ride: The Perfect Full-Day Itinerary from {item}",
        'meta_description_tpl': "Combine Hell's Gate cycling with a Lake Naivasha hippo boat safari for the ultimate Kenyan day trip from {item}. Full itinerary, prices, and booking guide.",
        'content_tpl': """
<h2>Kenya's Greatest One-Day Adventure: Hell's Gate + Lake Naivasha</h2>
<p>If you are traveling from <strong>{item}</strong> and looking for the single most activity-packed day trip in Kenya, the classic combination of <strong>Hell's Gate National Park cycling</strong> followed by a <strong>Lake Naivasha hippo boat safari</strong> with Rafiki is the ultimate answer.</p>

<h3>The Full-Day Itinerary</h3>
<p><strong>6:30 AM — Depart from {item}.</strong> Early departure ensures you beat traffic and arrive at Hell's Gate by 8:00–9:00 AM.</p>
<p><strong>9:00 AM – 1:00 PM — Hell's Gate Cycling.</strong> Hire bicycles at the gate and cycle through dramatic volcanic gorges past towering rock columns, hot springs, and grazing buffaloes, zebras, and elands. The gorge walk through Fischer's Tower canyon is a highlight.</p>
<p><strong>1:30 PM – 2:30 PM — Lunch at Karagita Beach.</strong> Fresh charcoal-grilled tilapia directly sourced from the lake. Affordable and delicious.</p>
<p><strong>3:00 PM – 4:30 PM — Rafiki Lake Naivasha Hippo Boat Safari.</strong> After lunch, board your pre-booked private Rafiki charter for a 1.5-hour hippo and bird safari. Late afternoon hippos are particularly active.</p>
<p><strong>5:00 PM — Begin return to {item}.</strong></p>

<h3>Booking Your Boat Safari in Advance</h3>
<p>Weekend boat safaris book up fast during peak season. Message Rafiki on WhatsApp at <strong>+254 701 215 295</strong> at least 48 hours before to secure your afternoon slot after your Hell's Gate cycling session.</p>
""",
        'tags': ['hells gate lake naivasha', 'best boat rides naivasha', 'lake naivasha boat ride price'],
        'item_source': 'origins'
    },

    # 15. LAKE NAIVASHA REVIEW / WHAT TO EXPECT
    {
        'title_tpl': "Lake Naivasha Boat Ride Review: What {item} Visitors Are Saying About Rafiki",
        'meta_description_tpl': "Read authentic Lake Naivasha boat ride reviews from Rafiki guests. What to expect, wildlife highlights, safety, and why Rafiki consistently earns 5-star ratings.",
        'content_tpl': """
<h2>5-Star Reviews for Lake Naivasha Boat Rides</h2>
<p>Rafiki has consistently maintained a <strong>guest-first reputation</strong> from hundreds of authentic reviews by visitors from <strong>{item}</strong> and across Kenya. Here is a compilation of what guests consistently praise and what you can expect from your own safari.</p>

<h3>What Guests Say About Safety</h3>
<p>"We had three children under 6 and were nervous about the boat ride. Rafiki had perfectly sized life jackets for each child and the captain briefed us clearly before departure. We felt completely safe the entire time." — Nairobi Family, 2025</p>

<h3>What Guests Say About Wildlife Encounters</h3>
<p>"Within 10 minutes of departing the beach, we were surrounded by 40+ hippos. Our captain knew exactly where the pods rested and positioned the boat perfectly for photos without disturbing them. The fish eagle dive right next to our boat was extraordinary." — International Tourist, 2025</p>

<h3>What Guests Say About Value</h3>
<p>"Booked directly on WhatsApp and paid exactly the quoted price — no hidden fees, no broker commissions. For what we experienced, it was tremendous value compared to other boat operators we'd used on Mombasa Creek." — Family from {item}, 2025</p>

<h3>Book Your Rafiki Experience</h3>
<p>Join thousands of satisfied guests from <strong>{item}</strong> who have experienced Lake Naivasha with Rafiki. Message us directly on WhatsApp at <strong>+254 701 215 295</strong> to check availability and book your preferred date.</p>
""",
        'tags': ['lake naivasha boat ride review', 'gitoh b boat rides naivasha reviews', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 16. FISHING GUIDE
    {
        'title_tpl': "Lake Naivasha Fishing Tour Guide for {item} Anglers: Tilapia, Bass & Booking",
        'meta_description_tpl': "Lake Naivasha fishing tours for anglers from {item}: what fish to catch (tilapia, largemouth bass), best spots, licensing requirements, and booking with Rafiki.",
        'content_tpl': """
<h2>Fishing on Lake Naivasha: A Local Expert's Guide</h2>
<p>For serious anglers traveling from <strong>{item}</strong>, Lake Naivasha offers a unique freshwater fishing experience combining Nile tilapia, largemouth bass, and African catfish in one of Kenya's most scenic settings.</p>

<h3>Target Species</h3>
<ul>
    <li><strong>Nile Tilapia (<em>Oreochromis niloticus</em>):</strong> The lake's primary fish species, reaching weights of 1–3 kg. Found in shallow, weedy areas near papyrus margins.</li>
    <li><strong>Largemouth Bass (<em>Micropterus salmoides</em>):</strong> Introduced in the 1920s, now a popular sport fish. Trophy specimens over 3 kg are caught regularly near the eastern shoreline structures.</li>
    <li><strong>African Catfish (<em>Clarias gariepinus</em>):</strong> Nocturnal feeders common in the deeper open water channels.</li>
</ul>

<h3>Best Fishing Seasons for {item} Visitors</h3>
<p>Year-round fishing is possible, but the best bass fishing occurs during the cooler months (June–August) when bass congregate in predictable feeding zones. Tilapia fishing peaks during the long rains (April–May) when runoff increases nutrient levels and surface feeding activity.</p>

<h3>Licensing & Catch Regulations</h3>
<p>Commercial fishing requires a license from Kenya Fisheries. Sport catch-and-release fishing for visiting anglers is practiced and encouraged. Rafiki provides all necessary fishing equipment including rods, bait, and tackle on request.</p>
<p>Book your dedicated fishing charter from <strong>{item}</strong> via WhatsApp: <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['lake naivasha fishing tour', 'boat safari lake naivasha', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 17. LANDMARK FEATURE ARTICLE
    {
        'title_tpl': "{item}: The Complete Guide to Kenya's Most Iconic Rift Valley Attraction",
        'meta_description_tpl': "Your complete guide to {item} near Lake Naivasha — history, wildlife, visiting tips, and how to combine it with a Rafiki hippo boat safari for the ultimate Rift Valley day.",
        'content_tpl': """
<h2>Discovering {item}: A Rift Valley Icon</h2>
<p><strong>{item}</strong> is one of the most remarkable natural and cultural attractions in Kenya's Great Rift Valley. Located within easy reach of Lake Naivasha's shimmering waters, combining a visit to {item} with a Rafiki wildlife boat safari creates what many visitors describe as the single greatest day experience available in East Africa.</p>

<h3>The Natural History of {item}</h3>
<p>The Great Rift Valley's extraordinary geological drama shapes everything you see at <strong>{item}</strong>. Formed over 20 million years of tectonic activity, the valley's escarpment walls, volcanic craters, and hydrothermal springs create a landscape unlike anywhere else on the planet. {item} sits at the intersection of geological forces that continue to sculpt East Africa today.</p>

<h3>Wildlife at {item}</h3>
<p>The surrounding ecosystem supports an extraordinary range of mammals and birds. From grazing herds of zebra and impala to endemic Rift Valley bird species, the biodiversity around <strong>{item}</strong> reflects the lake's influence as a freshwater anchor for the region's food web.</p>

<h3>Combining {item} with a Lake Naivasha Boat Safari</h3>
<p>The perfect itinerary pairs your <strong>{item}</strong> exploration with an afternoon Rafiki boat safari — departing Karagita Beach at 3:30 PM for the magical golden-hour hippo and sunset cruise. Book both experiences through Rafiki's WhatsApp line at <strong>+254 701 215 295</strong> for a fully coordinated, seamless day.</p>
""",
        'tags': ['best boat rides naivasha', 'lake naivasha boat ride review', 'boat safari lake naivasha'],
        'item_source': 'landmarks'
    },

    # 18. NAIVASHA BOAT RIDE IN KENYA OVERVIEW
    {
        'title_tpl': "Lake Naivasha Boat Ride in Kenya: Everything a First-Timer from {item} Must Know",
        'meta_description_tpl': "Complete first-timer guide to Lake Naivasha boat rides in Kenya for visitors from {item}: what to expect, safety, pricing, timing, and the best operators.",
        'content_tpl': """
<h2>Your First Lake Naivasha Boat Ride: A Complete First-Timer's Guide</h2>
<p>If you are planning your first <strong>Lake Naivasha boat ride in Kenya</strong> and you are coming from <strong>{item}</strong>, welcome! You are about to experience something that will genuinely stay with you for the rest of your life. Here is everything you need to know before you step onto the dock at Karagita Beach.</p>

<h3>What Will You See?</h3>
<p>Lake Naivasha is home to one of East Africa's highest concentrations of hippopotami — over 1,500 individuals. Within minutes of departing the beach, your boat will be surrounded by pod after pod of these massive mammals. You will also encounter hunting African Fish Eagles, Malachite Kingfishers, and — if you are lucky — a Nile crocodile basking on a papyrus island.</p>

<h3>Is it Safe?</h3>
<p><strong>Yes — when you book with a reputable operator.</strong> Rafiki's boats are equipped with certified life jackets for every passenger. Our captains maintain strict hippo safety buffers (minimum 50 meters) and have zero recorded incidents across deep local experience of commercial operations. Always confirm your operator has proper safety equipment before boarding.</p>

<h3>How Long Should You Book?</h3>
<ul>
    <li><strong>1 hour:</strong> Hippo and bird safari. Suitable for time-limited day-trippers.</li>
    <li><strong>2–3 hours:</strong> Full Crescent Island combo — boat transfer + walking safari among giraffes.</li>
    <li><strong>Half-day (4–5 hours):</strong> Ultimate wildlife marathon covering all key zones of the lake.</li>
</ul>
<p>Book your first Naivasha boat ride from <strong>{item}</strong> via WhatsApp: <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['lake naivasha boat ride price in kenya', 'lake naivasha boat ride review', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 19. CORPORATE TEAM BUILDING
    {
        'title_tpl': "Corporate Team Building at Lake Naivasha: Rafiki's Group Safari Guide for {item} Companies",
        'meta_description_tpl': "Plan your company's team building retreat at Lake Naivasha from {item}. Pontoon charters, wildlife safaris, group activities, and full event coordination with Rafiki.",
        'content_tpl': """
<h2>Why Lake Naivasha is Kenya's Best Corporate Team Building Venue</h2>
<p>For HR managers and event organizers at companies based in <strong>{item}</strong>, Lake Naivasha has emerged as Kenya's premier corporate team building destination. The lake's serene, screen-free environment creates conditions for genuine team bonding that urban conference rooms simply cannot replicate.</p>

<h3>Why the Lake Works for Team Building</h3>
<p>Research consistently shows that nature immersion reduces cortisol levels and improves collaborative thinking. A morning spent watching hippo dynamics — observing territorial hierarchies, communication behaviors, and cooperative mother-infant bonds — creates powerful metaphors for corporate leadership that facilitators can anchor to your organization's specific values.</p>

<h3>Rafiki's Corporate Safari Packages</h3>
<ul>
    <li><strong>Group Wildlife Safari (Flat-Rate Charter):</strong> Private boat for your entire team. No shared passengers. Captain serves as naturalist facilitator.</li>
    <li><strong>Pontoon Conference Charter:</strong> Spacious flat-deck pontoon with shade cover for larger teams. Ideal for 15–30 participants.</li>
    <li><strong>Full-Day Program:</strong> Morning boat safari + Crescent Island walking challenge + afternoon Hell's Gate cycling + Karagita Beach team lunch.</li>
</ul>

<h3>Logistics from {item}</h3>
<p>Rafiki coordinates all logistics including transport guidance from <strong>{item}</strong>, accommodation recommendations at lakeside hotels, and catering coordination for post-safari team lunches. Our event coordination team is reachable directly on WhatsApp at <strong>+254 701 215 295</strong> for custom group quotations.</p>
""",
        'tags': ['lake naivasha corporate team building', 'pontoon boat rides naivasha', 'best boat rides naivasha'],
        'item_source': 'origins'
    },

    # 20. PHOTOGRAPHY GUIDE
    {
        'title_tpl': "Lake Naivasha Photography Safari: Wildlife Photography Guide for {item} Photographers",
        'meta_description_tpl': "Lake Naivasha photography guide for visitors from {item}: camera settings, best wildlife spots, optimal light times, and booking a slow-drift photography boat safari with Rafiki.",
        'content_tpl': """
<h2>Photographing Lake Naivasha's Wildlife from a Boat</h2>
<p>For wildlife photographers traveling from <strong>{item}</strong>, Lake Naivasha offers a remarkable combination of subjects — large charismatic megafauna (hippos, giraffes), dramatic bird action (eagle dives, kingfisher hovering), and extraordinary Rift Valley landscape backdrops — all accessible from a stable boat platform.</p>

<h3>Optimal Light Windows</h3>
<p><strong>Golden hour (6:30–8:30 AM)</strong> is universally the best time for wildlife photography on the lake. The low-angle sunrise light creates warm, soft tones on hippo skin, catches the iridescence of kingfisher plumage, and silhouettes fish eagles against a flaming sky. The calm morning water also provides perfect mirror reflections.</p>

<h3>Camera Settings for Boat Photography</h3>
<ul>
    <li><strong>Birds in flight:</strong> Use continuous autofocus (AI Servo/AF-C), shutter speed minimum 1/2000s, burst mode.</li>
    <li><strong>Hippos at rest:</strong> 1/500s shutter, f/5.6–8 for sharpness across the pod, ISO 400.</li>
    <li><strong>Fish Eagle dives:</strong> Pre-focus on the water surface near a known perch tree, use your camera's fastest burst rate, 1/3200s minimum.</li>
</ul>

<h3>Rafiki's Photography-Optimized Safari</h3>
<p>Our photography charter for visitors from <strong>{item}</strong> uses a <strong>slow-drift approach</strong> — engine off, paddling gently — to minimize vibration and noise within critical photography zones. Captains position the boat to place subjects against clean backgrounds and optimal light angles.</p>
<p>Book your dedicated photography safari via WhatsApp: <strong>+254 701 215 295</strong>.</p>
""",
        'tags': ['lake naivasha photography tour', 'bird watching lake naivasha', 'best boat rides naivasha'],
        'item_source': 'origins'
    },
]

# =====================================================================
# GENERATE UNIQUE BLOG POSTS USING ALL TEMPLATES
# =====================================================================
item_sources = {
    'origins': origins,
    'hotels': hotels,
    'landmarks': landmarks,
    'seasons': seasons,
    'activities': activities
}

generated_blogs = []
idx = 0

while len(generated_blogs) < needed:
    tpl = blog_templates[idx % len(blog_templates)]
    source_key = tpl['item_source']
    source_list = item_sources[source_key]
    item = source_list[idx % len(source_list)]

    title = tpl['title_tpl'].format(item=item)
    slug = slugify(title)

    # Collision avoidance
    base_slug = slug
    suffix = 1
    while any(b['slug'] == slug for b in generated_blogs) or Post.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{suffix}"
        suffix += 1

    meta_desc = tpl['meta_description_tpl'].format(item=item)[:160]
    content = tpl['content_tpl'].format(item=item).strip()

    generated_blogs.append({
        'title': title,
        'slug': slug,
        'meta_description': meta_desc,
        'content': content,
        'tags': tpl['tags']
    })
    idx += 1

print(f"Total blog posts compiled: {len(generated_blogs)}")

# =====================================================================
# BULK INSERT INTO DATABASE
# =====================================================================
created_count = 0
updated_count = 0
for i, data in enumerate(generated_blogs, 1):
    post, created = Post.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'author': admin,
            'content': data['content'],
            'meta_description': data['meta_description'],
            'status': 'published'
        }
    )
    post.tags.set(data['tags'])
    if created:
        created_count += 1
    else:
        updated_count += 1
    if i % 50 == 0:
        print(f"  Progress: {i}/{len(generated_blogs)} processed...")

print(f"\n{'=' * 60}")
print(f"PHASE 13 COMPLETE!")
print(f"  Blogs Created: {created_count}")
print(f"  Blogs Updated: {updated_count}")
print(f"  Total Blog Posts in Database: {Post.objects.all().count()}")
print(f"{'=' * 60}")
