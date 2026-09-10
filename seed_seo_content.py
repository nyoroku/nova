"""
SEO Content Seeder — Creates blog posts, FAQs, and local pages
targeting the top 52 GBP search keywords for Rafiki Boat Rides Naivasha.

Run: .venv\Scripts\python.exe seed_seo_content.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from seo.models import FAQ, LocalPage, InternalLink

admin = User.objects.filter(is_superuser=True).first()
if not admin:
    seed_password = os.environ.get('DJANGO_SEED_ADMIN_PASSWORD')
    if not seed_password:
        raise RuntimeError('Set DJANGO_SEED_ADMIN_PASSWORD before creating the seed admin user.')
    admin = User.objects.create_superuser('admin', 'admin@rafikiboatride.com', seed_password)

# ====================================================================
#  BLOG POSTS — targeting top keyword clusters
# ====================================================================
blog_posts = [
    {
        'title': 'Hippo Boat Tour on Lake Naivasha — What to Expect',
        'slug': 'hippo-boat-tour-lake-naivasha',
        'meta_description': 'Join a hippo boat tour on Lake Naivasha with Rafiki. See hippos up close, spot 400+ bird species, and enjoy a safe, guided wildlife boat safari in Naivasha.',
        'content': """
<h2>The Ultimate Hippo Boat Tour on Lake Naivasha</h2>

<p>Lake Naivasha is home to one of Kenya's largest hippo populations, and a <strong>hippo boat tour</strong> is the best way to see these magnificent creatures in their natural habitat. At Rafiki Boat Rides Naivasha, we've been guiding visitors through these waters for many seasons — and we know exactly where the hippos are.</p>

<h3>What You'll See on a Hippo Boat Safari</h3>

<p>Our experienced guides take you through the quieter channels of Lake Naivasha where hippo pods gather. On a typical <strong>boat safari Lake Naivasha</strong>, you can expect to see:</p>

<ul>
<li><strong>Hippo pods</strong> — Often 10-30 hippos basking or submerged, surfacing with their signature snort</li>
<li><strong>African Fish Eagles</strong> — The iconic call of the Fish Eagle is the soundtrack of every boat ride</li>
<li><strong>Pelicans and cormorants</strong> — Hundreds line the shores and papyrus beds</li>
<li><strong>Monitor lizards</strong> — Occasionally spotted sunning on the shoreline</li>
<li><strong>Crescent Island wildlife</strong> — Giraffes, zebras, and wildebeest visible from the water</li>
</ul>

<h3>Safety on Our Hippo Boat Tours</h3>

<p>Safety is our top priority. Our captains maintain a respectful distance from all wildlife, and every passenger wears a life jacket. Our boats are well-maintained and inspected regularly. We've guided over many guests safely — your adventure with Rafiki is in experienced hands.</p>

<h3>Best Time for a Hippo Boat Tour</h3>

<p>The best times for a <strong>boat ride on Lake Naivasha</strong> to see hippos are early morning (6:30 AM – 9:00 AM) and late afternoon (3:00 PM – 6:00 PM). During these hours, hippos are most active and the light is perfect for photography.</p>

<h3>How to Book Your Hippo Safari</h3>

<p>Booking is easy — WhatsApp us at <strong>+254 701 215 295</strong> or browse our tours online. We offer both private and group <strong>boat rides in Naivasha</strong>, with prices starting from KES 1,000 per person.</p>

<p>Whether you're a wildlife enthusiast, photographer, or simply looking for the <strong>best boat ride Naivasha</strong> has to offer — a hippo boat tour with Rafiki is an experience you'll never forget.</p>
"""
    },
    {
        'title': 'Crescent Island Tour — Walking Safari from Lake Naivasha',
        'slug': 'crescent-island-tour-walking-safari-naivasha',
        'meta_description': 'Book a Crescent Island tour from Lake Naivasha with Rafiki. Boat transfer + walking safari among giraffes, zebras & wildebeest. No fences, just wildlife.',
        'content': """
<h2>Crescent Island Tour — A Walking Safari Like No Other</h2>

<p>Imagine stepping off a boat and walking freely among giraffes, zebras, and wildebeest — no fences, no vehicles, just you and the wildlife. That's exactly what a <strong>Crescent Island tour</strong> offers, and it starts with a scenic <strong>boat ride on Lake Naivasha</strong> with Rafiki.</p>

<h3>What Is Crescent Island?</h3>

<p>Crescent Island is a privately owned wildlife sanctuary on Lake Naivasha. It's technically a peninsula that becomes an island when water levels are high. The island is famous for being a filming location for the movie "Out of Africa" and is now one of Kenya's most unique safari destinations.</p>

<h3>What to Expect on Your Crescent Island Tour</h3>

<ol>
<li><strong>Scenic boat transfer</strong> — A 15-minute boat ride from Public Beach, Karagita, with hippo and bird sightings along the way</li>
<li><strong>Walking safari</strong> — Walk freely among wildlife for 1-2 hours. No guides required (though we recommend one for the best experience)</li>
<li><strong>Photography paradise</strong> — Get incredibly close to giraffes, zebras, waterbuck, elands, and wildebeest</li>
<li><strong>Bird watching</strong> — The island is home to over 100 bird species including the rare Verreaux's Eagle Owl</li>
<li><strong>Return boat ride</strong> — Enjoy the golden-hour light on your return trip</li>
</ol>

<h3>Crescent Island Tour Pricing</h3>

<p>The tour includes both the <strong>boat ride Lake Naivasha</strong> transfer and Crescent Island entry fees. Contact us on WhatsApp (+254 701 215 295) for current group and private rates.</p>

<h3>Best Time to Visit Crescent Island</h3>

<p>Morning visits (7:00 AM – 10:00 AM) offer the best wildlife activity and cooler temperatures. Late afternoon visits (3:00 PM – 5:30 PM) provide stunning golden light for photography.</p>

<p>Book your <strong>Crescent Island tour</strong> with Rafiki Boat Rides Naivasha and experience one of Kenya's most unique wildlife encounters!</p>
"""
    },
    {
        'title': 'Sunrise & Sunset Boat Rides on Lake Naivasha',
        'slug': 'sunrise-sunset-boat-rides-lake-naivasha',
        'meta_description': 'Experience magical sunrise and sunset boat rides on Lake Naivasha with Rafiki. Golden hour cruises perfect for couples, birthdays, and photography.',
        'content': """
<h2>Sunrise & Sunset Boat Rides — Lake Naivasha's Golden Hours</h2>

<p>There's something magical about watching the sun paint Lake Naivasha in shades of gold and amber from the deck of a boat. Our <strong>sunrise and sunset boat rides</strong> are among the most popular experiences we offer at Rafiki Boat Rides Naivasha.</p>

<h3>Sunrise Boat Ride (6:30 AM – 8:30 AM)</h3>

<p>The <strong>sunrise boat ride Lake Naivasha</strong> is for early risers and serious photographers. As the first light breaks over the Aberdare Mountains, the lake transforms into a mirror of pink and gold. This is when:</p>

<ul>
<li>Hippos are most active before retreating to deeper waters</li>
<li>Fish Eagles begin their morning hunt with dramatic calls</li>
<li>The lake is perfectly still — ideal for reflection photography</li>
<li>Fishermen cast their nets, creating iconic silhouettes</li>
</ul>

<h3>Sunset Cruise (4:00 PM – 6:30 PM)</h3>

<p>Our <strong>sunset cruises on Lake Naivasha</strong> are the most romantic experience on the lake. Perfect for:</p>

<ul>
<li><strong>Couples and proposals</strong> — Private boats with champagne available on request</li>
<li><strong>Birthdays and celebrations</strong> — Group cruises with snacks and music</li>
<li><strong>Photography enthusiasts</strong> — The golden hour light on the lake is unmatched</li>
<li><strong>Families</strong> — A peaceful, memorable way to end a day in Naivasha</li>
</ul>

<h3>What Makes Our Sunset Cruises Special</h3>

<p>Unlike other <strong>boat rides Naivasha</strong> operators, we take you to the quieter western channels where you can enjoy the sunset without engine noise. Our guides know the secret spots where the light is most spectacular, and we time the trip so you arrive at the perfect viewpoint just as the sun begins to set.</p>

<h3>Book Your Golden Hour Experience</h3>

<p>Whether it's a <strong>sunrise boat ride</strong> or <strong>sunset cruise</strong>, these are our most-requested experiences. Book early via WhatsApp (+254 701 215 295) to secure your spot — especially on weekends and holidays.</p>
"""
    },
    {
        'title': 'Best Places to Visit in Naivasha with Friends — Complete Guide',
        'slug': 'best-places-visit-naivasha-friends',
        'meta_description': 'Discover the best places to visit in Naivasha with friends — boat rides, Crescent Island, Hell\'s Gate, hot springs & more. Plan your group trip today.',
        'content': """
<h2>Best Places to Visit in Naivasha with Friends</h2>

<p>Planning a group trip to Naivasha? Whether it's a birthday celebration, team-building outing, or just a fun weekend getaway, Naivasha has something for everyone. Here's our insider guide to the <strong>best places to visit in Naivasha with friends</strong>.</p>

<h3>1. Lake Naivasha Boat Ride</h3>

<p>No visit to Naivasha is complete without a <strong>boat ride on Lake Naivasha</strong>. At Rafiki Boat Rides, we offer group packages that include hippo watching, bird spotting, and scenic lake cruises. Groups of 6+ get special rates — contact us for a quote!</p>

<h3>2. Crescent Island Walking Safari</h3>

<p>Walk freely among giraffes, zebras, and wildebeest on <strong>Crescent Island</strong>. It's one of the most unique safari experiences in Kenya, and the boat transfer from Public Beach is an adventure in itself. Perfect for Instagram-worthy group photos!</p>

<h3>3. Hell's Gate National Park</h3>

<p>Rent bikes and cycle through Hell's Gate gorge, past towering cliffs and hot springs. It's one of the few parks in Kenya where you can walk and cycle among wildlife. The gorge hike is a must-do for adventurous friend groups.</p>

<h3>4. Olkaria Geothermal Spa</h3>

<p>After an active morning, relax at the natural hot springs powered by geothermal activity. The warm waters are the perfect way to unwind after a <strong>boat ride Lake Naivasha</strong> or a hellish hike through the gorge.</p>

<h3>5. Naivasha Public Beach</h3>

<p>The <strong>Lake Naivasha beach</strong> area at Karagita is where most boat rides depart. It's a lively spot with food vendors, souvenir shops, and stunning lake views. Meet your Rafiki guide here for your <strong>boat tour Naivasha</strong>.</p>

<h3>6. Elsamere Conservation Centre</h3>

<p>The former home of Joy Adamson (Born Free). Visit for afternoon tea, learn about conservation, and enjoy the beautiful gardens on the shores of Lake Naivasha.</p>

<h3>7. Mt. Longonot Hike</h3>

<p>For the fitness enthusiasts in your group — climb the volcanic crater of Mt. Longonot. The 1-2 hour hike rewards you with 360° views of the Great Rift Valley and Lake Naivasha.</p>

<h3>Plan Your Naivasha Group Trip</h3>

<p>We can help you plan the perfect <strong>Naivasha tour package</strong> that combines boat rides with other activities. WhatsApp us at +254 701 215 295 for custom group itineraries.</p>
"""
    },
    {
        'title': 'Naivasha Tour Packages — Complete Lake Naivasha Experience',
        'slug': 'naivasha-tour-packages-lake-naivasha-experience',
        'meta_description': 'Book complete Naivasha tour packages with Rafiki — boat rides, Crescent Island, sunset cruises & wildlife safaris. Day trips from Nairobi available.',
        'content': """
<h2>Naivasha Tour Packages — Your Complete Lake Experience</h2>

<p>Looking for a complete <strong>Naivasha tour</strong> that combines the best activities around <strong>Lake Naivasha</strong>? Rafiki Boat Rides offers curated packages that give you the full experience — from wildlife boat safaris to walking safaris and sunset cruises.</p>

<h3>Half-Day Package (3-4 Hours)</h3>

<p>Perfect for day-trippers from Nairobi. This package includes:</p>

<ul>
<li>1-hour <strong>boat ride Lake Naivasha</strong> with hippo and bird watching</li>
<li>Boat transfer to Crescent Island + 1-hour walking safari</li>
<li>Return boat transfer with scenic route</li>
</ul>

<h3>Full-Day Lake Package (6-7 Hours)</h3>

<p>The ultimate <strong>Lake Naivasha tour</strong> for those who want to see it all:</p>

<ul>
<li>Morning <strong>boat safari Lake Naivasha</strong> — hippos, birds, fishermen</li>
<li>Crescent Island walking safari</li>
<li>Lunch break (we recommend lakeside restaurants)</li>
<li>Afternoon <strong>sunset cruise</strong> with golden-hour photography</li>
</ul>

<h3>Romantic Couples Package</h3>

<p>Designed for anniversaries, proposals, and honeymoons:</p>

<ul>
<li>Private <strong>sunset cruise Naivasha</strong> for two</li>
<li>Champagne and snacks on board</li>
<li>Dedicated photographer available (on request)</li>
<li>Scenic route through lily pads and papyrus channels</li>
</ul>

<h3>Group & Corporate Package</h3>

<p>Team building, birthday parties, or friend group weekends:</p>

<ul>
<li>Multiple boats for large groups</li>
<li>Custom itineraries</li>
<li>Combined <strong>boat rides</strong> + Hell's Gate cycling</li>
<li>Special rates for groups of 10+</li>
</ul>

<h3>Day Trip from Nairobi</h3>

<p>Lake Naivasha is just 1.5 hours from <strong>Nairobi</strong>, making it the perfect day trip destination. We can arrange pickup from Nairobi or meet you at Public Beach, Karagita.</p>

<h3>Book Your Package</h3>

<p>All packages are customizable. Contact us on WhatsApp (+254 701 215 295) to design your perfect <strong>Naivasha tour package</strong>. We'll handle the boats — you just bring your sense of adventure.</p>
"""
    },
]

print("--- Creating Blog Posts ---")
for data in blog_posts:
    post, created = Post.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'author': admin,
            'content': data['content'].strip(),
            'meta_description': data['meta_description'],
            'status': 'published',
        }
    )
    action = "CREATED" if created else "UPDATED"
    print(f"  [{action}] {post.title}")


# ====================================================================
#  FAQs — targeting question-based keyword searches
# ====================================================================
faqs = [
    {
        'question': 'How much does a boat ride in Naivasha cost?',
        'answer': '<p>Boat ride prices in Naivasha vary depending on the type and duration. At Rafiki Boat Rides Naivasha, our rates start from <strong>KES 1,000 per person per hour</strong> for group rides. Private boat charters, sunset cruises, and Crescent Island transfers are priced separately. We accept cash (KES/USD), M-Pesa, and bank transfers. Contact us on WhatsApp (+254 701 215 295) for exact pricing and group discounts.</p>',
        'plain_answer': 'Boat ride prices at Rafiki start from KES 1,000 per person per hour. Private charters and special packages vary. We accept cash, M-Pesa, and bank transfers.',
        'search_intent': 'pricing',
        'order': 1,
    },
    {
        'question': 'What is the best time for a boat ride at Lake Naivasha?',
        'answer': '<p>The best times for a <strong>boat ride at Lake Naivasha</strong> are early morning (6:30 AM – 9:00 AM) and late afternoon (3:00 PM – 6:30 PM). Early mornings offer calm waters, active wildlife, and beautiful sunrise light. Late afternoons provide the famous golden-hour sunset views. For hippo watching specifically, early morning is ideal as hippos are most active before retreating to deeper waters. We operate daily from <strong>6:30 AM to 6:30 PM</strong>.</p>',
        'plain_answer': 'The best times are early morning (6:30-9AM) for wildlife activity and late afternoon (3-6:30PM) for sunset views. We operate daily 6:30AM-6:30PM.',
        'search_intent': 'timing',
        'order': 2,
    },
    {
        'question': 'How do I get to Lake Naivasha from Nairobi?',
        'answer': '<p>Lake Naivasha is approximately <strong>90 km from Nairobi</strong>, about a 1.5-hour drive via the Nairobi-Nakuru Highway (A104). You can drive yourself, take a matatu (public bus) from Nairobi\'s Mololine terminus, or hire a private taxi. Once in Naivasha town, head to <strong>Public Beach, Karagita</strong> where Rafiki Boat Rides operates. We can provide directions — just WhatsApp us at +254 701 215 295.</p>',
        'plain_answer': 'Lake Naivasha is 1.5 hours from Nairobi via the Nairobi-Nakuru Highway. Drive, take a matatu, or hire a taxi. Our launch point is at Public Beach, Karagita.',
        'search_intent': 'location',
        'order': 3,
    },
    {
        'question': 'Can I see hippos on a Lake Naivasha boat ride?',
        'answer': '<p>Yes! Hippos are the main attraction on Lake Naivasha <strong>boat rides</strong>. The lake has one of Kenya\'s largest hippo populations, and our guides know exactly where the pods gather. You\'ll typically see hippos submerging, surfacing, and yawning during your <strong>boat safari</strong>. Our experienced captains maintain a safe distance while giving you perfect viewing and photography angles. Hippo sightings are virtually guaranteed on every trip.</p>',
        'plain_answer': 'Yes! Hippos are virtually guaranteed on every boat ride. Lake Naivasha has one of Kenya\'s largest hippo populations and our guides know exactly where they gather.',
        'search_intent': 'wildlife',
        'order': 4,
    },
    {
        'question': 'What animals can I see at Crescent Island?',
        'answer': '<p>Crescent Island is a unique wildlife sanctuary where you can walk freely among animals — no fences or vehicles needed. You\'ll see <strong>giraffes, zebras, wildebeest, waterbuck, elands, impalas</strong>, and a variety of bird species. The boat transfer from Public Beach to <strong>Crescent Island</strong> also offers hippo and bird sightings along the way. It\'s one of the most Instagrammable experiences in Kenya!</p>',
        'plain_answer': 'At Crescent Island you can walk among giraffes, zebras, wildebeest, waterbuck, elands, and impalas. The boat transfer also includes hippo and bird watching.',
        'search_intent': 'wildlife',
        'order': 5,
    },
    {
        'question': 'Are boat rides in Naivasha safe for children?',
        'answer': '<p>Absolutely! Rafiki Boat Rides Naivasha is <strong>family-friendly</strong> and we welcome children of all ages. We provide life jackets in all sizes, and our experienced captains prioritize safety above everything. Our boats are well-maintained and regularly inspected. For families with young children (under 5), we recommend private boat charters so you can control the pace and duration. We\'ve safely hosted over many guests including many families.</p>',
        'plain_answer': 'Yes, boat rides with Rafiki are safe for children. We provide life jackets in all sizes, use well-maintained boats, and offer private charters for families with young children.',
        'search_intent': 'safety',
        'order': 6,
    },
    {
        'question': 'Do you offer boat rides near me in Naivasha?',
        'answer': '<p>If you\'re in or near Naivasha, Rafiki Boat Rides is located at <strong>Public Beach, Lake, Karagita</strong> — the main boat launch point on Lake Naivasha. We\'re easily accessible from Naivasha town (10-minute drive), nearby hotels, and lodges. Our <strong>boat rides</strong> depart daily from 6:30 AM to 6:30 PM. You can walk in or book ahead via WhatsApp (+254 701 215 295) to guarantee your spot.</p>',
        'plain_answer': 'We operate from Public Beach, Karagita, Naivasha — the main boat launch point. Open daily 6:30AM-6:30PM. Book via WhatsApp or walk in.',
        'search_intent': 'location',
        'order': 7,
    },
    {
        'question': 'What is the difference between boat ride and boat safari on Lake Naivasha?',
        'answer': '<p>A <strong>boat ride</strong> is a general scenic cruise on Lake Naivasha, while a <strong>boat safari</strong> specifically focuses on wildlife viewing — hippos, birds, and other lake creatures. At Rafiki, every <strong>boat ride in Lake Naivasha</strong> includes elements of a safari, as our guides actively point out wildlife along the way. We also offer dedicated <strong>hippo boat tours</strong>, <strong>bird watching safaris</strong>, and combined <strong>boat ride + Crescent Island walking safari</strong> packages.</p>',
        'plain_answer': 'A boat ride is a scenic cruise, while a boat safari focuses on wildlife viewing. At Rafiki, every ride includes wildlife spotting. We also offer dedicated hippo and bird watching safaris.',
        'search_intent': 'booking',
        'order': 8,
    },
    {
        'question': 'Can I book a boat ride for a birthday or special event?',
        'answer': '<p>Yes! We offer <strong>private boat charters</strong> for birthdays, anniversaries, proposals, corporate events, and other celebrations. Our private charters include a dedicated boat, experienced guide, and can be customized with extras like champagne, music, and photography. We\'ve hosted memorable celebrations on Lake Naivasha — just tell us what you need! Book via WhatsApp (+254 701 215 295) at least 24 hours in advance for special events.</p>',
        'plain_answer': 'Yes, we offer private charters for birthdays, anniversaries, proposals, and corporate events. Customize with champagne, music, and photography. Book 24 hours in advance.',
        'search_intent': 'booking',
        'order': 9,
    },
    {
        'question': 'What should I wear for a boat ride in Naivasha?',
        'answer': '<p>For your <strong>boat ride in Naivasha</strong>, we recommend: comfortable, layered clothing (mornings and evenings can be cool); a hat and sunglasses for sun protection; sunscreen (SPF 30+); comfortable closed-toe shoes or sandals with grip; a light waterproof jacket (in case of light spray); and insect repellent. Bring a camera or phone for photos — our guides can help you get the best shots. We provide life jackets for everyone.</p>',
        'plain_answer': 'Wear comfortable, layered clothing, a hat, sunglasses, sunscreen, and closed-toe shoes. Bring a camera and insect repellent. We provide life jackets.',
        'search_intent': 'preparation',
        'order': 10,
    },
    {
        'question': 'How long is a typical boat ride on Lake Naivasha?',
        'answer': '<p>A typical <strong>boat ride on Lake Naivasha</strong> lasts 1-2 hours, depending on the package. Here\'s a breakdown: a <strong>standard boat ride</strong> (hippo and bird watching) is 1 hour; a <strong>Crescent Island tour</strong> (boat transfer + walking safari) is 2-3 hours; a <strong>sunset cruise</strong> is 1.5-2 hours; and a <strong>full-day lake package</strong> is 5-7 hours. All durations can be customized to your preference.</p>',
        'plain_answer': 'Standard rides are 1 hour, Crescent Island tours 2-3 hours, sunset cruises 1.5-2 hours, and full-day packages 5-7 hours. All can be customized.',
        'search_intent': 'timing',
        'order': 11,
    },
]

print("\n--- Creating FAQs ---")
for data in faqs:
    faq, created = FAQ.objects.update_or_create(
        question=data['question'],
        defaults={
            'answer': data['answer'],
            'plain_answer': data['plain_answer'],
            'search_intent': data['search_intent'],
            'order': data['order'],
            'is_active': True,
            'allow_indexing': True,
        }
    )
    action = "CREATED" if created else "UPDATED"
    print(f"  [{action}] {faq.question}")

# Fix old Njovic FAQ
old_faq = FAQ.objects.filter(question__icontains='Njovic').first()
if old_faq:
    old_faq.question = old_faq.question.replace('Njovic Boats', 'Rafiki').replace('Njovic', 'Rafiki')
    old_faq.answer = old_faq.answer.replace('Njovic Boats', 'Rafiki Boat Rides').replace('Njovic', 'Rafiki')
    old_faq.save()
    print(f"  [FIXED] Renamed Njovic reference to Rafiki")


# ====================================================================
#  LOCAL PAGES — targeting location + service keyword combos
# ====================================================================
local_pages = [
    {
        'title': 'Lake Naivasha Beach — Public Beach Boat Launch',
        'slug': 'lake-naivasha-beach',
        'seo_title': 'Lake Naivasha Beach | Public Beach Karagita — Boat Rides & Tours',
        'meta_description': 'Visit Lake Naivasha Beach at Karagita — the main launch point for boat rides, hippo safaris & Crescent Island tours. Find directions, hours & booking info.',
        'primary_keyword': 'lake naivasha beach',
        'location': 'Public Beach, Karagita, Naivasha',
        'modifiers': 'beach, public beach, boat launch, karagita',
        'content': """
<h2>Lake Naivasha Beach — Your Gateway to the Lake</h2>

<p><strong>Lake Naivasha Beach</strong>, locally known as Public Beach at Karagita, is the main launch point for boat rides on the lake. This is where Rafiki Boat Rides Naivasha operates, and where your lake adventure begins.</p>

<h3>Getting Here</h3>

<p>Public Beach is located approximately 10 minutes from Naivasha town center, in the Karagita area. From the main Nairobi-Nakuru highway, take the Lake Road turnoff and follow signs to the Public Beach. Plenty of parking is available.</p>

<h3>What to Expect at the Beach</h3>

<p>The beach area is a lively hub with boat operators, food vendors, souvenir shops, and scenic lake views. You'll find:</p>

<ul>
<li>Boat operators (look for the Rafiki Boat Rides sign!)</li>
<li>Fresh fish restaurants serving tilapia straight from the lake</li>
<li>Views of hippos near the shore</li>
<li>Scenic photo spots with Mt. Longonot in the background</li>
</ul>

<h3>Boat Rides from Public Beach</h3>

<p>All Rafiki <strong>boat rides in Naivasha</strong> depart from here. Choose from hippo safaris, sunset cruises, Crescent Island transfers, and photography tours. We operate daily from 6:30 AM to 6:30 PM.</p>

<p>WhatsApp us at +254 701 215 295 to book your <strong>boat ride at Lake Naivasha</strong> from Public Beach.</p>
"""
    },
    {
        'title': 'Bird Watching on Lake Naivasha',
        'slug': 'bird-watching-lake-naivasha',
        'seo_title': 'Bird Watching Lake Naivasha | 400+ Species — Boat Tours & Safaris',
        'meta_description': 'Lake Naivasha is home to 400+ bird species. Join a dedicated bird watching boat tour with Rafiki — Fish Eagles, pelicans, flamingos & more.',
        'primary_keyword': 'bird watching lake naivasha',
        'location': 'Lake Naivasha',
        'modifiers': 'birds, bird safari, ornithology, fish eagle, pelicans',
        'content': """
<h2>Bird Watching on Lake Naivasha — A Birder's Paradise</h2>

<p>Lake Naivasha is recognized as an Important Bird Area (IBA) by BirdLife International, home to over <strong>400 bird species</strong>. For bird enthusiasts, a <strong>boat ride on Lake Naivasha</strong> is essentially a floating bird hide with front-row seats to some of Africa's most spectacular avian life.</p>

<h3>Star Species to Spot</h3>

<ul>
<li><strong>African Fish Eagle</strong> — The legendary raptor with its iconic call, frequently seen plunging into the lake for fish</li>
<li><strong>Great White Pelicans</strong> — Hundreds congregate on the lake shores, fishing in coordinated groups</li>
<li><strong>Malachite Kingfisher</strong> — Tiny, jewel-colored birds perched on papyrus reeds</li>
<li><strong>Pied Kingfisher</strong> — Hovering above the water before diving for fish</li>
<li><strong>African Jacana</strong> — "Jesus bird" that walks on lily pads</li>
<li><strong>Grey Herons and Goliath Herons</strong> — Standing sentinel in the shallows</li>
<li><strong>Cormorants</strong> — Lines of dozens drying their wings on dead trees</li>
<li><strong>Pink-backed Pelicans</strong> — Nesting in the papyrus at the eastern shores</li>
</ul>

<h3>Our Bird Watching Boat Tours</h3>

<p>At Rafiki Boat Rides Naivasha, our guides are trained bird spotters who know the habitats, feeding patterns, and seasonal movements. We offer dedicated <strong>bird watching boat safaris</strong> that go slower and quieter, visiting the best birding channels and papyrus beds.</p>

<h3>Best Time for Bird Watching</h3>

<p>Early morning (6:30 AM – 9:00 AM) is peak birding time. Migratory species are present November through March, adding to the resident population. The rainy seasons (March-May, October-November) bring the greatest diversity.</p>

<p>Book your bird watching <strong>boat tour Naivasha</strong> with Rafiki — WhatsApp +254 701 215 295.</p>
"""
    },
    {
        'title': 'Boat Safari Lake Naivasha — Wildlife & Nature Tours',
        'slug': 'boat-safari-lake-naivasha',
        'seo_title': 'Boat Safari Lake Naivasha | Hippos, Birds & Wildlife Tours — Rafiki',
        'meta_description': 'Experience the best boat safari on Lake Naivasha with Rafiki. See hippos, 400+ bird species, and stunning landscapes. Book your wildlife boat tour today.',
        'primary_keyword': 'boat safari lake naivasha',
        'location': 'Lake Naivasha',
        'modifiers': 'safari, wildlife, hippo, nature, tour',
        'content': """
<h2>Boat Safari Lake Naivasha — Into the Wild</h2>

<p>A <strong>boat safari on Lake Naivasha</strong> is one of Kenya's most accessible and affordable wildlife experiences. Unlike a traditional game drive, you're gliding across water, approaching wildlife from a unique perspective that's both intimate and safe.</p>

<h3>What Makes Our Boat Safaris Special</h3>

<p>Rafiki Boat Rides has been guiding <strong>Lake Naivasha safaris</strong> for many seasons. Our advantage:</p>

<ul>
<li><strong>Local expertise</strong> — Our guides grew up on these waters and know every channel, hippo pod, and eagle nest</li>
<li><strong>Small groups</strong> — Maximum 8 people per boat for a personal experience</li>
<li><strong>Safe boats</strong> — Well-maintained vessels with life jackets for all</li>
<li><strong>Flexible routes</strong> — We adjust based on wildlife activity and weather</li>
</ul>

<h3>Safari Routes</h3>

<p>Our guides choose from several routes based on conditions:</p>

<ol>
<li><strong>Hippo Channel Route</strong> — Through the papyrus channels to the main hippo pods</li>
<li><strong>Crescent Island Circuit</strong> — Around the island with views of giraffes, zebras, and birds</li>
<li><strong>Fisherman's Route</strong> — Past local fishing communities and pelican colonies</li>
<li><strong>Sunset Route</strong> — Western channels for the best golden-hour views</li>
</ol>

<h3>Boat Safari Pricing</h3>

<p>Our <strong>boat safari Lake Naivasha</strong> rates start from KES 1,000 per person. Private safaris and extended tours are available at custom rates. We accept cash, M-Pesa, and bank transfers.</p>

<h3>Book Your Safari</h3>

<p>Ready for your <strong>Lake Naivasha tour</strong>? WhatsApp us at +254 701 215 295 or browse our tours online. We operate daily from 6:30 AM to 6:30 PM at Public Beach, Karagita.</p>
"""
    },
]

print("\n--- Creating Local Pages ---")
for data in local_pages:
    page, created = LocalPage.objects.update_or_create(
        slug=data['slug'],
        defaults={
            'title': data['title'],
            'seo_title': data['seo_title'],
            'meta_description': data['meta_description'],
            'primary_keyword': data['primary_keyword'],
            'location': data['location'],
            'modifiers': data['modifiers'],
            'content': data['content'].strip(),
            'is_active': True,
            'allow_indexing': True,
        }
    )
    action = "CREATED" if created else "UPDATED"
    print(f"  [{action}] {page.title}")


# ====================================================================
#  INTERNAL LINKS — for auto-linking across all content
# ====================================================================
internal_links = [
    {'keyword': 'boat ride Naivasha', 'url': '/'},
    {'keyword': 'boat rides Naivasha', 'url': '/'},
    {'keyword': 'boat ride Lake Naivasha', 'url': '/tours/'},
    {'keyword': 'boat rides Lake Naivasha', 'url': '/tours/'},
    {'keyword': 'Lake Naivasha boat ride', 'url': '/tours/'},
    {'keyword': 'hippo boat tour', 'url': '/blog/hippo-boat-tour-lake-naivasha/'},
    {'keyword': 'Crescent Island', 'url': '/crescent-island-tours/'},
    {'keyword': 'Crescent Island tour', 'url': '/blog/crescent-island-tour-walking-safari-naivasha/'},
    {'keyword': 'sunset cruise', 'url': '/sunset-cruises-naivasha/'},
    {'keyword': 'sunset cruise Naivasha', 'url': '/sunset-cruises-naivasha/'},
    {'keyword': 'boat safari Lake Naivasha', 'url': '/boat-safari-lake-naivasha/'},
    {'keyword': 'bird watching Lake Naivasha', 'url': '/bird-watching-lake-naivasha/'},
    {'keyword': 'Lake Naivasha beach', 'url': '/lake-naivasha-beach/'},
    {'keyword': 'Naivasha tour packages', 'url': '/blog/naivasha-tour-packages-lake-naivasha-experience/'},
    {'keyword': 'best places to visit in Naivasha', 'url': '/blog/best-places-visit-naivasha-friends/'},
]

print("\n--- Creating Internal Links ---")
for data in internal_links:
    link, created = InternalLink.objects.update_or_create(
        keyword=data['keyword'],
        defaults={
            'url': data['url'],
            'is_active': True,
        }
    )
    action = "CREATED" if created else "UPDATED"
    print(f"  [{action}] '{link.keyword}' -> {link.url}")


print("\n✅ SEO Content Seeding Complete!")
print(f"   Blog Posts: {Post.objects.filter(status='published').count()} total")
print(f"   FAQs: {FAQ.objects.filter(is_active=True).count()} total")
print(f"   Local Pages: {LocalPage.objects.filter(is_active=True).count()} total")
print(f"   Internal Links: {InternalLink.objects.filter(is_active=True).count()} total")
