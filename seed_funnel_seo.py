"""
Programmatic SEO (pSEO) & Funnel Keyword Seeder
Creates 3 detailed blog posts, 3 local pages, FAQs, and internal links.
Run: .venv\\Scripts\\python.exe seed_funnel_seo.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from seo.models import FAQ, LocalPage, InternalLink

# Get superuser
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    seed_password = os.environ.get('DJANGO_SEED_ADMIN_PASSWORD')
    if not seed_password:
        raise RuntimeError('Set DJANGO_SEED_ADMIN_PASSWORD before creating the seed admin user.')
    admin = User.objects.create_superuser('admin', 'admin@rafikiboatride.com', seed_password)

# ====================================================================
#  INTERNAL LINKS
# ====================================================================
new_links = [
    ('Madaraka Day Naivasha', '/blog/things-to-do-naivasha-madaraka-day-holidays/'),
    ('Watamu Boat Ride', '/blog/lake-naivasha-boat-ride-comparison-rafiki-watamu-njovic/'),
    ('Njovic Boat Ride', '/blog/lake-naivasha-boat-ride-comparison-rafiki-watamu-njovic/'),
    ('Crescent Island Walking Safari', '/seo/crescent-island-walking-safari/'),
    ('Karagita Public Beach', '/seo/karagita-public-beach/'),
    ('Sanctuary Farm Lake Naivasha', '/seo/sanctuary-farm-lake-naivasha/'),
]

print("--- Creating/Updating Internal Links ---")
for kw, url in new_links:
    link, created = InternalLink.objects.update_or_create(
        keyword=kw,
        defaults={'url': url, 'is_active': True}
    )
    action = "NEW" if created else "UPD"
    print(f"  [{action}] '{kw}' -> {url}")


# ====================================================================
#  BLOG POSTS (approx 500+ words each)
# ====================================================================
blog_posts = [
    {
        'title': 'Top Things to Do in Naivasha During Madaraka Day & Public Holidays',
        'slug': 'things-to-do-naivasha-madaraka-day-holidays',
        'meta_description': 'Planning a Nairobi getaway for Madaraka Day or Easter? Discover the best things to do in Naivasha, including Hippo boat safaris, Hell\'s Gate, and Crescent Island.',
        'tags': ['things to do in Naivasha', 'Madaraka Day Naivasha', 'weekend getaways near Nairobi', 'Lake Naivasha tour'],
        'content': """
<h2>Make the Most of Your Madaraka Day & Public Holiday Getaway in Naivasha</h2>

<p>Every year as national public holidays like <strong>Madaraka Day Naivasha</strong> (June 1st), Mashujaa Day (October 20th), Jamhuri Day (December 12th), or the Easter and Christmas seasons approach, thousands of Nairobi residents look for the perfect weekend getaway. Located just 90 kilometers northwest of the capital, Naivasha stands out as the ultimate destination for holidaymakers seeking adventure, wildlife, and natural beauty without the stress of long travel times. The scenic descent down the Great Rift Valley escarpment sets the tone for a refreshing holiday break.</p>

<h3>The Ultimate Holiday Itinerary in Naivasha</h3>
<p>To enjoy a rewarding holiday in Naivasha, you need a diverse itinerary that blends active exploration with peaceful relaxation. Start your day early at <strong>Hell's Gate National Park</strong>. Famous for its towering red cliffs, deep gorges, and geothermal activity, Hell's Gate is one of the few national parks in Kenya where visitors can cycle directly past herds of zebras, giraffes, and gazelles. Cycling through the park is an exhilarating adventure that is highly popular for family groups during long weekends.</p>

<p>After a morning of cycling and hiking through the gorges, head down to the lake shore for the highlight of any Naivasha excursion: a guided hippo boat safari. Taking a private boat ride from <strong>Karagita Public Beach</strong> puts you face-to-face with the lake's famous hippo pods. You can also disembark at the peninsula for a remarkable <strong>Crescent Island Walking Safari</strong>, where you can walk alongside giraffes, wildebeests, and waterbucks in complete safety.</p>

<h3>Why Boat Safaris are the Heart of Naivasha Tourism</h3>
<p>Unlike other dry-land safaris, a boat safari on Lake Naivasha offers a fresh, dynamic perspective of Kenya's wildlife. As you glide smoothly through the calm waters, your certified captain will point out diverse bird species—from the majestic African Fish Eagle swooping down to catch fish to elegant Great White Pelicans swimming in formation. It is a peaceful yet thrilling experience that appeals to children, couples, and photography enthusiasts alike, making it the perfect focal point for a holiday weekend.</p>

<h3>Pro Tips for Public Holiday Booking</h3>
<p>Because Naivasha is incredibly popular during public holidays like Madaraka Day, bookings can fill up extremely quickly. Hotels, camps, and quality boat ride services experience a huge surge in demand. To ensure a smooth trip, follow these important holiday travel tips:</p>
<ul>
    <li><strong>Book Your Boat in Advance:</strong> Avoid long queues and holiday surge pricing by reserving your boat ride slot with a trusted operator like Rafiki Boat Rides before you travel.</li>
    <li><strong>Depart Nairobi Early:</strong> The A104 highway can experience heavy holiday traffic. Departing Nairobi by 6:00 AM ensures you beat the traffic and arrive in Naivasha in time for the calmest morning waters.</li>
    <li><strong>Combine Activities:</strong> Look for combo packages that include a boat ride transfer, Crescent Island walking tour, and lunch to save time and money.</li>
</ul>
<p>Whether you're celebrating Madaraka Day, spending Easter with family, or planning a festive Christmas retreat, Lake Naivasha offers the perfect blend of escape and adventure just a short drive from Nairobi.</p>
"""
    },
    {
        'title': 'Lake Naivasha Boat Ride Comparison: Rafiki, Watamu, and Njovic',
        'slug': 'lake-naivasha-boat-ride-comparison-rafiki-watamu-njovic',
        'meta_description': 'Compare the top Lake Naivasha boat ride operators: Rafiki, Watamu, and Njovic. Discover differences in pricing, safety, wildlife knowledge, and client reviews.',
        'tags': ['best boat rides Lake Naivasha', 'Watamu Boat Ride', 'Njovic Boat Ride', 'Rafiki Boat Rides'],
        'content': """
<h2>Which Boat Ride Operator in Naivasha Should You Choose?</h2>

<p>If you're planning a trip to Lake Naivasha, booking a boat ride is undoubtedly the best way to see the lake\'s incredible hippo pods and abundant birdlife. However, with multiple operators advertising online and along the shoreline, choosing the right service can be confusing. To help you make an informed decision, we have put together an honest, detailed comparison of the top three digital boat operators on the lake: <strong>Rafiki Boat Rides</strong>, <strong>Watamu Boat Ride</strong>, and <strong>Njovic Boat Ride</strong>.</p>

<h3>1. Rafiki Boat Rides: The Local, Woman-Owned Trust Leader</h3>
<p>Operating directly from the accessible <strong>Karagita Public Beach</strong>, Rafiki Boat Rides has built an outstanding reputation as the lake's most reliable and transparent operator. As a woman-owned business, Rafiki places a heavy emphasis on safety, local employment, and customer satisfaction. With a flawless guest-first reputation across nearly a hundred verified Google reviews, they are the undisputed leaders in customer trust.</p>
<ul>
    <li><strong>Pricing Structure:</strong> Extremely transparent, flat-rate pricing per boat (approx. KES 3,000 to KES 8,000 per hour depending on boat size) rather than confusing per-person rates.</li>
    <li><strong>Safety Standards:</strong> Exemplary. Mandatory, high-quality life jackets for all passengers (including specialized sizes for kids), certified captains, and sturdy flat-bottomed boats.</li>
    <li><strong>Unique Value:</strong> Customized itineraries (like sunset golden hour photography cruises) and captains who are highly knowledgeable about the lake\'s bird and hippo populations.</li>
</ul>

<h3>2. Watamu Boat Ride: The Rapid Transit Option</h3>
<p><strong>Watamu Boat Ride</strong> (led by local guide Tony Watamu) is another established player on the lake. They specialize in fast, efficient transfers across the lake, making them a popular choice for visitors who want a quick trip to Crescent Island.</p>
<ul>
    <li><strong>Strengths:</strong> Good digital booking system, fast communication, and reliable transfers.</li>
    <li><strong>Weaknesses:</strong> Pricing can sometimes be less transparent online, with rates varying based on season and negotiations. They focus more on standard transport than custom, relaxed wildlife photography safaris.</li>
</ul>

<h3>3. Njovic Boat Ride: The Circuit Specialists</h3>
<p>Operating on the lake for over 8 years, <strong>Njovic Boat Ride</strong> markets itself on detailed "Full Circuit" tours that cover Hippo Point, Oloidien, and Crescent Island. They have a detailed website and a good collection of blog guides.</p>
<ul>
    <li><strong>Strengths:</strong> Diverse package options and highly educational captains.</li>
    <li><strong>Weaknesses:</strong> Their digital presence is heavily warning-based due to a high volume of online fraudsters impersonating their brand. They lack the extensive, verified third-party Google Maps review history that Rafiki boasts, making verification slightly harder for first-time visitors.</li>
</ul>

<h3>The Verdict: Why Rafiki Boat Rides Wins on Value and Safety</h3>
<p>While all three operators offer access to the beautiful waters of Lake Naivasha, <strong>Rafiki Boat Rides</strong> stands out as the best choice for families, private groups, and photographers. Their flat-rate per boat pricing ensures you get the absolute best value without hidden charges, and their verified guest-first reputation offers peace of mind that you are booking a safe, professional, and genuinely local experience. When planning your Naivasha trip, skip the unverified shoreline brokers and book directly with Rafiki for a seamless adventure on the water.</p>
"""
    },
    {
        'title': 'How to Book the Safest & Most Affordable Hippo Boat Safari in Naivasha',
        'slug': 'how-to-book-safest-affordable-hippo-boat-safari',
        'meta_description': 'Learn how to book a safe, affordable hippo boat safari on Lake Naivasha. Avoid shoreline scams, understand flat-rate pricing, and enjoy your wildlife safari.',
        'tags': ['book boat safari Lake Naivasha', 'Lake Naivasha boat ride price', 'Rafiki Boat Rides booking', 'hippo safari Lake Naivasha'],
        'content': """
<h2>Your Complete Guide to Booking a Hippo Boat Safari on Lake Naivasha</h2>

<p>A hippo boat safari on Lake Naivasha is one of the most rewarding wildlife experiences in Kenya. Because Lake Naivasha is a freshwater lake, it hosts a booming population of over 1,500 hippos and more than 400 species of birds. Best of all, unlike national parks, there are no Kenya Wildlife Service (KWS) gate entry fees for the lake itself—you only pay for your boat ride! This makes it an incredibly affordable activity. However, navigating the booking process and avoiding shoreline brokers can be tricky. This guide covers exactly how to book a safe, affordable tour.</p>

<h3>Avoid Shoreline Brokers & Scams</h3>
<p>When you arrive at public beaches like <strong>Karagita Public Beach</strong>, you will often be approached by dozens of aggressive shoreline brokers or informal agents claiming to offer the "cheapest boat ride." These brokers do not own boats; instead, they add massive commissions to the price and often book you onto uncertified, crowded boats without proper safety gear. To ensure your safety and get the best price, always book directly with a registered operator like Rafiki Boat Rides before you arrive. Legitimate operators will assign you a certified captain who will meet you directly at a designated parking area.</p>

<h3>Understand Flat-Rate Boat Pricing</h3>
<p>One of the easiest ways to get ripped off is by agreeing to a "per-person" rate for a private group. Standard motorized boats on Lake Naivasha comfortably carry up to 6 or 7 passengers. Legitimate operators charge a flat, transparent rate per boat per hour (typically KES 3,000 to KES 5,000 for standard tours). If a broker quotes you a per-person rate for a group of 5, you will end up paying double or triple the actual boat value. Always insist on flat-rate boat pricing to keep your trip affordable.</p>

<h3>Key Safety Requirements to Verify</h3>
<p>Safety should never be compromised for a cheap price. Hippos are highly territorial and dangerous animals. Ensure your boat operator meets the following criteria:</p>
<ul>
    <li><strong>Mandatory Life Jackets:</strong> The operator must provide well-fitting, high-buoyancy life jackets for every passenger, including children. Do not board a boat without one.</li>
    <li><strong>Certified Captains:</strong> Your captain must be licensed by the maritime authority and have extensive experience navigating the lake\'s shallow waters and reading hippo behavior.</li>
    <li><strong>Safe Distances:</strong> A professional captain will always maintain a safe distance of at least 30 meters from hippo pods, ensuring the animals are not agitated while allowing you to capture stunning photos.</li>
</ul>

<h3>How to Secure Your Booking with Rafiki</h3>
<p>Booking a premium safari with Rafiki Boat Rides is simple and stress-free. Send a WhatsApp message to their booking office at <strong>+254 729 280 380</strong>. Specify your preferred date, time, and group size. They will provide a flat, all-inclusive quote and assign a professional captain to guide you through the beautiful western channels, hippo pools, and bird-nesting areas. Reserve your slot today for the ultimate Lake Naivasha experience!</p>
"""
    }
]

print("\n--- Creating/Updating Blog Posts ---")
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
    post.tags.set(data['tags'])
    action = "NEW" if created else "UPD"
    print(f"  [{action}] {post.title} (Slug: {post.slug})")


# ====================================================================
#  LOCAL PAGES (approx 500+ words each)
# ====================================================================
local_pages = [
    {
        'title': 'Crescent Island Walking Safari',
        'slug': 'crescent-island-walking-safari',
        'seo_title': 'Crescent Island Walking Safari Lake Naivasha (2026 Guide)',
        'meta_description': 'Guide to Crescent Island Walking Safari on Lake Naivasha. See giraffes, zebras, waterbucks up close. Boat transfers, entry fees, and booking info.',
        'primary_keyword': 'Crescent Island Walking Safari',
        'location': 'Crescent Island, Lake Naivasha',
        'modifiers': 'walking safari, boat transfer, entrance fee, giraffes, wild animals',
        'content': """
<h2>Walk Among Wild Animals at Crescent Island Game Sanctuary</h2>

<p>Often described as Naivasha's best-kept secret, the <strong>Crescent Island Walking Safari</strong> offers one of the most unique wildlife experiences in all of East Africa. Located on a beautiful, crescent-shaped volcanic peninsula on Lake Naivasha, this private sanctuary is entirely free of predators. This unique geographical feature allows visitors of all ages to embark on a guided foot safari, walking directly alongside peaceful herds of giraffes, zebras, wildebeests, waterbucks, and impalas. It is a breathtaking experience that feels like walking through a real-life scene from the Lion King.</p>

<h3>How to Access Crescent Island</h3>
<p>Because the sanctuary is surrounded by the waters of Lake Naivasha, the most scenic and convenient way to access it is by boat. Booking a boat transfer with Rafiki Boat Rides allows you to enjoy a thrilling 20-minute hippo safari and bird-watching cruise before landing directly on the shores of Crescent Island. The boat will drop you off at the sanctuary entrance, where you will pay your entry fees and meet a resident guide, and then wait to transport you safely back to the mainland after your walk.</p>

<h3>The Foot Safari Experience</h3>
<p>Once you step onto the island, the sense of tranquility is immediate. Guided by an experienced local naturalist, you will follow gentle dirt paths that wind through acacia forests and open grassy plains. Because the animals have been protected here for decades, they are remarkably calm and accustomed to human presence. You can easily approach within safe, respectful distances of Maasai giraffes grazing on acacia leaves, zebras grooming each other, and majestic African Fish Eagles nesting in the high branches above. It is a paradise for wildlife photographers and nature lovers.</p>

<h3>Key Travel Logistics: Fees & Hours</h3>
<p>To plan a successful visit to the Crescent Island sanctuary, keep the following logistical details in mind:</p>
<ul>
    <li><strong>Entrance Fees (2026):</strong> Non-resident adults pay USD 30, while Kenyan citizens and residents pay KES 1,000. Children pay discounted rates. Note that these entry fees are paid directly to the sanctuary at the gate and are separate from your boat transfer fee.</li>
    <li><strong>Opening Hours:</strong> The sanctuary is open daily from 8:30 AM to 5:30 PM. The best time to visit is early morning (between 8:30 AM and 10:30 AM) when the weather is cool, the animals are highly active, and the lake waters are calm.</li>
    <li><strong>What to Wear:</strong> Wear comfortable walking shoes, a wide-brimmed sun hat, sunscreen, and carry a bottle of drinking water. Do not forget your camera or binoculars!</li>
</ul>

<h3>Book Your Crescent Island Combo Tour</h3>
<p>Rafiki Boat Rides offers highly recommended Crescent Island combo packages that cover your private boat transfer, a guided hippo and bird-watching boat tour, safe parking, and seamless gate coordinates. Contact their booking office on WhatsApp at <strong>+254 729 280 380</strong> to plan a memorable walking safari today.</p>
"""
    },
    {
        'title': 'Karagita Public Beach',
        'slug': 'karagita-public-beach',
        'seo_title': 'Karagita Public Beach Lake Naivasha: Tilapia, Boats & Parking',
        'meta_description': 'Visit Karagita Public Beach, the premier launch point for Lake Naivasha boat rides. Secure parking, fresh grilled tilapia, local fish market, and safaris.',
        'primary_keyword': 'Karagita Public Beach',
        'location': 'Karagita Beach, Lake Naivasha',
        'modifiers': 'tilapia, boat launch, secure parking, local food, fish market',
        'content': """
<h2>Discover the Vibrant Heart of Lake Naivasha at Karagita Public Beach</h2>

<p>Located on the bustling southern shores of the lake, <strong>Karagita Public Beach</strong> is the primary public access point and the energetic hub of local tourism and fishing on Lake Naivasha. Unlike private hotel shores, Karagita is a lively, culturally rich public beach where local fishermen, boat captains, craft vendors, and fish fryers gather daily. For travelers, visiting Karagita offers an authentic, sensory introduction to the vibrant community that depends on the freshwater ecosystem of the Great Rift Valley.</p>

<h3>The Best Place for Fresh Lakeside Tilapia</h3>
<p>One of the biggest highlights of visiting Karagita Beach is the local culinary experience. The beach is famous for its open-air fish market, where local women cook freshly caught Lake Naivasha tilapia over open charcoal grills. Served hot with a side of traditional ugali and kachumbari (tomato and onion salad), eating fresh tilapia by the water is an absolute must-do activity for both local and international tourists. The fish is incredibly affordable, delicious, and provides direct support to the hardworking women of the Karagita community.</p>

<h3>The Premier Boat Ride Launching Ground</h3>
<p>Because of its strategic geographic location and flat shorelines, Karagita is the main launching point for Lake Naivasha boat rides and safaris. From the shores of Karagita, boats can quickly and easily reach the lake\'s main hippo habitats, Oloidien channels, and the Crescent Island game sanctuary. Reputable operators, including the highly rated Rafiki Boat Rides, base their fleets of modern, fiberglass boats directly at Karagita Beach. This ensures quick departures and extremely competitive flat-rate pricing on all boat charters.</p>

<h3>Visitor Logistics: Parking & Safety</h3>
<p>Visiting a busy public beach can sometimes feel overwhelming for first-time travelers. Follow these simple guidelines to ensure a safe, relaxed, and enjoyable experience at Karagita:</p>
<ul>
    <li><strong>Secure Vehicle Parking:</strong> Karagita Beach features a spacious, secure public parking area guarded by local community youth. Parking is highly safe, allowing you to leave your vehicle securely while you spend hours out on the water.</li>
    <li><strong>Avoid Beach Solicitation:</strong> The shoreline can have informal brokers trying to upsell uncertified boat rides. Always book your ride with a registered operator like Rafiki Boat Rides in advance. Your assigned captain will meet you directly at the parking area, shielding you from aggressive brokers.</li>
    <li><strong>Lakeside Walkways:</strong> Take a stroll along the grassy banks of the beach to observe local fishermen repairing their nets, and spot pelicans wading in the shallows waiting for fish scraps.</li>
</ul>

<h3>Experience Naivasha with Rafiki at Karagita</h3>
<p>Rafiki Boat Rides operates daily from 6:30 AM to 6:30 PM at Karagita Public Beach. Their professional team ensures you enjoy secure parking, delicious local tilapia, and safe, top-tier boat safaris. Book your trip by messaging <strong>+254 729 280 380</strong> on WhatsApp and experience Lake Naivasha like a local.</p>
"""
    },
    {
        'title': 'Sanctuary Farm Lake Naivasha',
        'slug': 'sanctuary-farm-lake-naivasha',
        'seo_title': 'Sanctuary Farm Lake Naivasha: Horse Riding, Birds & Eco-Safaris',
        'meta_description': 'Guide to Sanctuary Farm Lake Naivasha. Horseback riding among wildlife, bird watching, camping, and private boat rides in quiet papyrus channels.',
        'primary_keyword': 'Sanctuary Farm Lake Naivasha',
        'location': 'Sanctuary Farm, Naivasha',
        'modifiers': 'horse riding, bird watching, camping, quiet boat ride, eco-tourism',
        'content': """
<h2>Experience Serenity and Eco-Tourism at Sanctuary Farm Lake Naivasha</h2>

<p>For travelers seeking a quiet, highly exclusive, and deeply peaceful retreat near the water, <strong>Sanctuary Farm Lake Naivasha</strong> stands out as a premier destination. Originally established as a dairy farm on the southern shores of the lake, Sanctuary Farm has been lovingly converted into an eco-friendly wildlife sanctuary and lodge. Surrounded by towering yellow-fever acacia trees and lush green pastures, this private sanctuary offers a tranquil escape from the busier public beaches, making it a favorite for couples, bird watchers, and nature enthusiasts.</p>

<h3>A Haven for Bird Watching and Walking Safaris</h3>
<p>Sanctuary Farm is incredibly rich in biodiversity. Because the farm is bordered by quiet papyrus swamps, it attracts over 350 species of birds. Visitors can spend hours bird watching along the lakeshore, spotting colorful kingfishers, elegant herons, spoonbills, and the iconic African Fish Eagle. In addition to birding, guests can enjoy peaceful walking safaris through the farm\'s forests, walking alongside free-roaming giraffes, zebras, wildebeests, and waterbucks that graze peacefully on the pastures.</p>

<h3>Horseback Riding Among Wildlife</h3>
<p>One of the most famous and unique activities offered at Sanctuary Farm is horseback riding. Riding a well-trained horse directly past herds of zebras and giraffes is an unforgettable experience. Because the wild animals are accustomed to the presence of horses, they do not feel threatened, allowing riders to get remarkably close to the wildlife in complete safety and silence. The farm caters to all experience levels, from beginners to advanced riders.</p>

<h3>Quiet Boat Safaris in Papyrus Channels</h3>
<p>The shoreline of Sanctuary Farm features some of the lake's quietest and most scenic western channels. Booking a private boat ride that launches near the farm allows you to navigate narrow channels lined with dense papyrus reeds. This is the absolute best environment for spotting nesting birds and observing sleeping hippo pods up close without the noise and traffic of busier tourist boats. It is a highly intimate, romantic, and relaxing boat ride experience.</p>

<h3>Visiting Logistics & Booking</h3>
<p>Sanctuary Farm charges a modest day-visitor entry fee of KES 1,000 for adults, which goes directly toward supporting the sanctuary\'s conservation efforts. If you are staying at their beautiful campsite or boutique lodge, this fee is waived. To combine a tranquil visit to Sanctuary Farm with a premium hippo boat safari, book a customized tour with Rafiki Boat Rides. Rafiki can pick you up directly from lakeside coordinates and guide you through the lake\'s most pristine corners. Contact Rafiki on WhatsApp at <strong>+254 729 280 380</strong> to book your eco-safari today.</p>
"""
    }
]

print("\n--- Creating/Updating Local Pages ---")
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
    action = "NEW" if created else "UPD"
    print(f"  [{action}] {page.title} (Slug: {page.slug})")


# ====================================================================
#  HIGH-INTENT FAQs
# ====================================================================
faq_data = [
    (
        "How do I book a boat ride for Madaraka Day, Easter, or Christmas holidays?",
        "<p>To secure a boat ride slot during major Kenyan holidays like <strong>Madaraka Day Naivasha</strong> (June 1st), Easter, or the Christmas festive season, we strongly recommend booking <strong>at least 48 to 72 hours in advance</strong>. Public holidays bring a massive influx of domestic tourists from Nairobi, and quality boat operators fill up very quickly. You can easily reserve your private boat ride with Rafiki by sending a WhatsApp message directly to <strong>+254 729 280 380</strong>. We will assign a certified captain and lock in your flat-rate price, protecting you from holiday price hikes.</p>",
        "Book at least 48-72 hours in advance for public holidays like Madaraka Day or Christmas. Send a WhatsApp to +254 729 280 380 to lock in your flat-rate price.",
        "booking",
        201
    ),
    (
        "How does Rafiki's pricing compare to Watamu and Njovic boat rides?",
        "<p>Rafiki Boat Rides offers highly competitive, transparent, <strong>flat-rate boat pricing per hour</strong> (typically ranging from KES 3,000 to KES 8,000 depending on boat capacity and tour length) rather than charging per person. Unlike some shoreline brokers or other operators who use flexible, non-transparent pricing based on seasonal negotiations, Rafiki keeps pricing completely flat and public. This ensures you get the absolute best value without hidden commissions, extra landing fees, or unexpected price hikes on holiday weekends.</p>",
        "Rafiki uses transparent, flat-rate pricing per boat per hour (KES 3,000 - 8,000) rather than per-person rates or seasonal flexible pricing used by competitors.",
        "pricing",
        202
    ),
    (
        "Is a boat ride on Lake Naivasha safe during windy weather or afternoons?",
        "<p><strong>Yes, boat rides on Lake Naivasha are highly safe</strong> when booking with a certified operator. However, Lake Naivasha is prone to strong afternoon winds (locally known as the Rift Valley breeze) which can create moderate waves between 2:00 PM and 5:00 PM. Rafiki Boat Rides captains monitor weather forecasts and wind speeds hourly. Our flat-bottomed fiberglass boats are designed for stability, and we enforce a strict <strong>100% mandatory life jacket policy</strong> for all passengers. For the calmest, smoothest water and the best hippo sightings, we always recommend booking your safari in the morning between 7:00 AM and 11:00 AM.</p>",
        "Yes. Morning rides (7:00 - 11:00 AM) are smoothest. Rafiki enforces a strict mandatory life jacket policy and monitors wind speeds hourly for safety.",
        "safety",
        203
    ),
    (
        "Can we eat fresh tilapia at Karagita Beach before or after our boat ride?",
        "<p><strong>Absolutely yes!</strong> <strong>Karagita Public Beach</strong> is famous for its vibrant open-air fish market where local women grill freshly caught tilapia over hot charcoal. Eating hot tilapia served with ugali and kachumbari right by the lakeshore is one of the most popular, authentic, and affordable dining experiences in Naivasha. Our captains can easily guide you to the safest, cleanest, and most popular local fish kitchens upon returning from your boat safari, ensuring a delicious and safe culinary adventure.</p>",
        "Absolutely! Karagita Beach is famous for its charcoal-grilled tilapia served with ugali. Our captains can guide you to the best local kitchens.",
        "logistics",
        204
    ),
    (
        "Should I book a private boat charter or a shared group ride?",
        "<p>If you are traveling in a group of 3 or more people, booking a <strong>private boat charter is highly recommended and offers the best value</strong>. Private charters give you complete control over your itinerary, allowing your captain to slow down for photography, spend extra time near specific hippo pods, or customize your drop-off coordinates. Standard boats carry up to 7 passengers flat-rate. If you are a solo traveler or a couple on a strict budget, joining a shared group ride (starting around KES 1,000 - 1,500 per person) is a great way to meet fellow travelers while splitting the boat cost.</p>",
        "Private charters are best for groups of 3+ (flat-rate KES 3,000 - 5,000), offering custom itineraries. Shared rides are perfect for solo travelers or couples on a budget.",
        "booking",
        205
    )
]

print("\n--- Creating/Updating FAQs ---")
for q, a, plain, intent, order in faq_data:
    faq, created = FAQ.objects.update_or_create(
        question=q,
        defaults={
            'answer': a,
            'plain_answer': plain,
            'search_intent': intent,
            'order': order,
            'is_active': True,
            'allow_indexing': True,
        }
    )
    action = "NEW" if created else "UPD"
    print(f"  [{action}] {faq.question}")

print("\n[SUCCESS] Funnel SEO Seeding Complete!")
total_posts = Post.objects.filter(status='published').count()
total_faqs = FAQ.objects.filter(is_active=True).count()
total_pages = LocalPage.objects.filter(is_active=True).count()
total_links = InternalLink.objects.filter(is_active=True).count()
print(f"   Database Status:")
print(f"   - Blog Posts: {total_posts} total")
print(f"   - FAQs: {total_faqs} total")
print(f"   - Local Pages: {total_pages} total")
print(f"   - Internal Links: {total_links} total")
