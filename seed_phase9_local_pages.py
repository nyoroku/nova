"""
Phase 9: New pSEO Local Pages
Targets keyword clusters not yet covered:
- Families / kids
- Honeymoon / couples / romance
- Corporate team building
- Photography tours
- Birthday / special occasions
- Private charter hire
- Hell's Gate + lake combo
- Fishing tours
- Oloidien Bay
- Hippo Point area
Run: .venv\\Scripts\\python.exe seed_phase9_local_pages.py
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import LocalPage, InternalLink

pages = [
    # ------------------------------------------------------------------ #
    # 1. FAMILY / KIDS
    # ------------------------------------------------------------------ #
    {
        'title': 'Lake Naivasha Boat Ride with Kids',
        'slug': 'lake-naivasha-boat-ride-with-kids',
        'seo_title': 'Lake Naivasha Boat Ride with Kids (Safe Family Guide 2026)',
        'meta_description': 'Is a Lake Naivasha boat ride safe for children? Yes! Child life jackets, flat-bottomed boats & hippo education. Book a family-friendly safari with Rafiki.',
        'primary_keyword': 'Lake Naivasha boat ride with kids',
        'location': 'Karagita Beach, Lake Naivasha',
        'modifiers': 'children, family, safe, life jackets, kids, baby',
        'content': """
<h2>The Perfect Family Adventure on Lake Naivasha</h2>

<p>A boat ride on Lake Naivasha is one of the safest, most educational, and most thrilling wildlife experiences you can give your children in Kenya. Unlike a Maasai Mara safari — where children must stay confined inside a vehicle — Lake Naivasha's calm, shallow waters allow families to explore wildlife up close, at their own pace, with no risk of encountering predators. The lake is a classroom without walls, and a <strong>family boat ride with Rafiki</strong> is consistently rated the most memorable experience by parents visiting Naivasha.</p>

<h3>Why Lake Naivasha is Perfect for Children</h3>
<p>The lake's gentle, freshwater ecosystem makes it a safe, controlled environment for young explorers. There are no dangerous currents, no waves, and no crocodiles on the main lake body. The most "dangerous" animal your children will encounter is a massive, grunting hippopotamus viewed safely from a comfortable distance on your motorized boat — an encounter guaranteed to trigger screams of delighted excitement from every child on board.</p>

<ul>
    <li><strong>Zero Crocodile Risk:</strong> Unlike Lake Baringo or the Mara River, Lake Naivasha is a freshwater ecosystem without established crocodile populations. Children can freely watch hippos without the additional anxiety of hidden reptile threats.</li>
    <li><strong>Spectacular Bird Education:</strong> With over 400 bird species, the lake is a living nature documentary. Children will spot massive African Fish Eagles, Great White Pelicans, Malachite Kingfishers, and African Spoonbills — all at close range.</li>
    <li><strong>Hippo Education:</strong> Rafiki captains explain hippo biology, behavior, and conservation in simple, engaging language. Children frequently leave the boat knowing more about hippos than their parents.</li>
</ul>

<h3>Child Safety Standards at Rafiki</h3>
<p>Rafiki Boat Rides holds the strongest child safety standards of any operator on the lake. Every child, regardless of age or size, is fitted with a <strong>properly sized, certified life jacket</strong> before boarding. Rafiki stocks infant-specific, toddler-sized, and child-sized life jackets — not the oversized adult jackets you will find on uncertified boats.</p>

<ul>
    <li><strong>Flat-Bottomed, Stable Hulls:</strong> All Rafiki safari boats use wide, commercial fiberglass hulls with an extremely low center of gravity. The boats do not rock or tip under normal conditions, making boarding and seating safe and comfortable for toddlers.</li>
    <li><strong>No Standing Policy:</strong> All passengers, including children, must remain seated during transit. Captains enforce this rule politely but firmly.</li>
    <li><strong>Age Minimum:</strong> Rafiki welcomes children of all ages, including babies in arms. Infants are held securely by parents and fitted with a specialized infant floatation device.</li>
</ul>

<h3>The Best Boat Ride Experience for Families</h3>
<p>For families with young children, Rafiki recommends booking a <strong>private morning boat charter</strong> between 7:00 AM and 10:00 AM. The morning hours offer the calmest water, the coolest temperatures, and the most active hippo and birdlife. A standard 2-hour family safari covers the main hippo pools, the Crescent Island shoreline, and the papyrus reed channels — packed with extraordinary sights that children will talk about for years.</p>

<p>After the boat safari, many families visit the <strong>Karagita Beach fish market</strong> where children can watch local fishermen bring in fresh tilapia and observe pelicans swooping for scraps — a completely free, authentic wildlife experience.</p>

<h3>Book Your Family Safari</h3>
<p>Booking a family boat ride with Rafiki is simple. Send a WhatsApp message to <strong>+254 701 215 295</strong> with your preferred date, time, and the ages of your children. Rafiki will pre-arrange the right-sized life jackets, confirm your slot, and ensure your captain is briefed on the educational commentary your children will love.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 2. HONEYMOON / ROMANTIC COUPLES
    # ------------------------------------------------------------------ #
    {
        'title': 'Romantic Boat Ride Lake Naivasha Honeymoon',
        'slug': 'romantic-boat-ride-lake-naivasha-honeymoon',
        'seo_title': 'Romantic Boat Ride Lake Naivasha | Honeymoon & Couples Safari',
        'meta_description': 'Plan the perfect Lake Naivasha honeymoon or anniversary boat ride. Private sunset cruise, champagne packages, hippo watching & golden-hour photography with Rafiki.',
        'primary_keyword': 'romantic boat ride Lake Naivasha honeymoon',
        'location': 'Lake Naivasha',
        'modifiers': 'couples, honeymoon, anniversary, romantic, sunset, champagne, private',
        'content': """
<h2>The Most Romantic Sunset on the Rift Valley</h2>

<p>Lake Naivasha at sunset is one of Africa's most breathtaking natural spectacles. As the enormous equatorial sun descends slowly towards the Mau Escarpment, it turns the entire surface of the lake into liquid gold and burning copper. Silhouettes of hippos rise and sink through the shimmering surface. African Fish Eagles call across the still water. For couples celebrating a honeymoon, anniversary, proposal, or Valentine's Day getaway, a <strong>private sunset boat ride on Lake Naivasha</strong> with Rafiki is an unforgettable, deeply romantic experience that no hotel package can replicate.</p>

<h3>The Private Sunset Cruise Experience</h3>
<p>Unlike busy, crowded shared boat rides, Rafiki's private honeymoon charters give couples an exclusive, intimate experience on the water. Your captain will navigate the quietest, most scenic channels of the lake — far from tourist traffic — while you sit together watching the wildlife and the golden-hour light transform the landscape around you.</p>

<ul>
    <li><strong>Exclusive Boat:</strong> Your private vessel seats up to 7 people, but for couples, it is entirely yours. There are no strangers, no competing commentary, and no rush to move to the next spot.</li>
    <li><strong>Flexible Duration:</strong> Couples can book 1-hour, 2-hour, or extended 3-hour golden-hour sunset charters. The 2-hour sunset charter (departing around 4:30 PM) is consistently the most popular for honeymooners.</li>
    <li><strong>Photography Focus:</strong> Your captain is briefed to position the boat for maximum photographic impact — catching the hippos, the reflections, and the silhouetted escarpment in the background simultaneously.</li>
</ul>

<h3>Champagne & Special Occasion Upgrades</h3>
<p>Rafiki offers tailored special occasion packages for couples. Simply inform the team when booking that you are celebrating a honeymoon, anniversary, or proposal. The team can coordinate with partner lodges to arrange:</p>
<ul>
    <li>Chilled champagne or sparkling wine served on the water</li>
    <li>Fresh fruit platters pre-loaded onto the boat</li>
    <li>Flower arrangements on the boat seats</li>
    <li>A professional water-based photoshoot during golden hour</li>
</ul>

<h3>After the Cruise: Romantic Naivasha Experiences</h3>
<p>Lake Naivasha is surrounded by stunning boutique lodges and eco-retreats perfect for honeymooners. After your sunset cruise, consider:</p>
<ul>
    <li><strong>Crater Lake Game Sanctuary:</strong> A surreal, intimate volcanic crater filled with turquoise water and flamingos — one of Kenya's most romantic hidden gems, just 20 minutes from the lake.</li>
    <li><strong>Sanctuary Farm Horseback Riding:</strong> Gallop on horseback alongside giraffes and zebras on the lakeshore at dawn — a profoundly unique couple's activity.</li>
    <li><strong>Hell's Gate Gorge Walk:</strong> A private walk through towering volcanic cliffs and natural hot springs — the secluded gorge section is especially magical for couples.</li>
</ul>

<h3>Book Your Romantic Charter</h3>
<p>To plan your perfect honeymoon or anniversary boat ride, contact Rafiki directly on WhatsApp at <strong>+254 701 215 295</strong>. The team will customize every detail — from departure time to special decorations — to ensure your experience on the water is as magical as the occasion itself.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 3. CORPORATE TEAM BUILDING
    # ------------------------------------------------------------------ #
    {
        'title': 'Lake Naivasha Corporate Team Building Boat Safari',
        'slug': 'lake-naivasha-corporate-team-building',
        'seo_title': 'Lake Naivasha Corporate Team Building | Group Boat Safaris',
        'meta_description': 'Book a Lake Naivasha corporate team building boat safari for your company. Multi-boat group packages, catering, photography, and Hell\'s Gate activities. Rafiki handles logistics.',
        'primary_keyword': 'Lake Naivasha corporate team building',
        'location': 'Lake Naivasha, Naivasha',
        'modifiers': 'corporate, team building, group, company, retreat, workshop, conference',
        'content': """
<h2>The Ultimate Corporate Escape from Nairobi</h2>

<p>Lake Naivasha — just 90 kilometers and under 2 hours from Nairobi's CBD — is Kenya's premier corporate retreat destination. Every year, hundreds of Nairobi-based companies from the banking, NGO, technology, and hospitality sectors choose Lake Naivasha for their annual team-building getaways. A <strong>Rafiki Boat Rides corporate group safari</strong> is consistently the centrepiece activity of every successful team-building program on the lake, offering the perfect blend of shared adventure, wildlife education, and strategic outdoor bonding.</p>

<h3>Multi-Boat Group Packages</h3>
<p>Rafiki operates multiple boats simultaneously for large corporate groups. Whether your team has 10 people or 80 people, Rafiki can deploy its entire fleet in synchronized convoy for a group safari that ensures no team member is left behind on land.</p>

<ul>
    <li><strong>Fleet Coordination:</strong> Groups up to 14 people (2 full boats), 21 people (3 boats), 42 people (6 boats), or custom deployments for 80+ person corporate retreats.</li>
    <li><strong>Radio Communication:</strong> Captains maintain radio contact across all boats, ensuring synchronized movements to hippo pods and photographic spots so every boat has the same premium experience.</li>
    <li><strong>Competitive Activities:</strong> Request a friendly inter-boat bird-spotting competition (guided by captains) or a photo contest — simple, fun group dynamics exercises that naturally encourage cross-departmental interaction.</li>
</ul>

<h3>Full Corporate Safari Package</h3>
<p>Rafiki works with established partner lodges on South Lake Road to create comprehensive full-day corporate packages that include:</p>
<ol>
    <li><strong>8:00 AM:</strong> Group boat safari (2 hours) — hippo watching, bird identification, escarpment photography</li>
    <li><strong>10:30 AM:</strong> Team breakfast at lakeside partner lodge — fresh tilapia, eggs, and local accompaniments</li>
    <li><strong>12:00 PM:</strong> Hell's Gate National Park cycling excursion (team relay races through the park) — physical, competitive, and memorable</li>
    <li><strong>3:00 PM:</strong> Team lunch and facilitated strategic planning session at the lodge conference facility</li>
    <li><strong>5:00 PM:</strong> Optional sunset boat safari for leadership teams and senior management</li>
</ol>

<h3>Why Companies Choose Rafiki for Team Building</h3>
<ul>
    <li><strong>Reliability:</strong> Corporate events have fixed schedules. Rafiki's fleet is maintained to the highest standards with backup motors available to prevent event disruptions.</li>
    <li><strong>Professionalism:</strong> All captains are briefed on corporate confidentiality. No audio recordings, client photos, or corporate team activities are shared externally.</li>
    <li><strong>Invoice & Receipt:</strong> Rafiki issues proper tax invoices with KRA PIN for corporate procurement compliance and expense reimbursement.</li>
    <li><strong>Logistics Management:</strong> Rafiki can coordinate vehicle transport from Nairobi, lodge bookings, catering, and park entry fees into a single consolidated quote.</li>
</ul>

<h3>Request a Corporate Group Quote</h3>
<p>To receive a detailed, itemized quote for your company's team-building event, contact Rafiki's corporate team on WhatsApp at <strong>+254 701 215 295</strong>. Please include your team size, preferred date, and any special requirements. Rafiki typically responds to corporate inquiries within 2 hours during business hours.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 4. PHOTOGRAPHY TOURS
    # ------------------------------------------------------------------ #
    {
        'title': 'Lake Naivasha Photography Tour Birds and Wildlife',
        'slug': 'lake-naivasha-photography-tour',
        'seo_title': 'Lake Naivasha Photography Tour | Birds, Hippos & Golden Hour',
        'meta_description': 'The ultimate Lake Naivasha photography tour for birders and wildlife photographers. Best times, lens recommendations, hippo shots & golden-hour positions with Rafiki.',
        'primary_keyword': 'Lake Naivasha photography tour',
        'location': 'Lake Naivasha',
        'modifiers': 'photography, birding, telephoto, golden hour, wildlife, hippo shots',
        'content': """
<h2>Africa's Most Photogenic Freshwater Lake</h2>

<p>Professional wildlife photographers, serious birders, and passionate hobbyists consistently rank Lake Naivasha among East Africa's top five photography destinations. The combination of <strong>400+ bird species</strong>, massive resident hippo pods, dramatic Great Rift Valley escarpment backdrops, and the extraordinary quality of equatorial golden-hour light creates a photographic environment that simply cannot be replicated anywhere else in Kenya at this price point.</p>

<p>A <strong>private Rafiki photography boat charter</strong> unlocks the full visual potential of the lake. Unlike crowded shared rides that rush past subjects, private photography charters allow your captain to hold position, rotate the boat for optimal light angles, and wait patiently for the perfect behavioral shot.</p>

<h3>The Golden Hour Window (6:30–9:00 AM)</h3>
<p>The single most important piece of advice for Lake Naivasha photographers: <strong>book the earliest possible morning slot.</strong></p>

<ul>
    <li><strong>Light Quality:</strong> Between 6:30 AM and 8:00 AM, the low-angle equatorial sun bathes every subject in warm, directional amber light — completely eliminating the harsh overhead shadows that ruin midday wildlife photography.</li>
    <li><strong>Water Surface:</strong> The lake is completely glassy and mirror-calm in the morning. Every hippo, bird, and papyrus reed is perfectly reflected, creating extraordinary mirror compositions impossible to achieve in the afternoon wind.</li>
    <li><strong>Animal Activity:</strong> Hippos are most active — and most visible at the surface — in the early morning before they sink low for daytime rest. Birds are feeding, flying, and displaying. African Fish Eagles are actively hunting and vocalizing.</li>
    <li><strong>Thermal Wind:</strong> Zero morning wind means you can use extremely slow shutter speeds for artistic motion-blur water shots without boat vibration ruining your frames.</li>
</ul>

<h3>The 10 Best Photography Subjects on the Lake</h3>
<ol>
    <li><strong>African Fish Eagle (Haliaeetus vocifer):</strong> Perches on dead acacia branches overhanging the water. Use 500mm+ for close head portraits. The call is Africa's most iconic sound.</li>
    <li><strong>Great White Pelicans:</strong> Form massive, synchronized feeding formations of 50–200 birds. The morning light through their translucent wings is extraordinary.</li>
    <li><strong>Hippo Pod at Dawn:</strong> Position your boat 40–50 meters from the pod with the escarpment silhouetted in the background for classic African wildlife compositions.</li>
    <li><strong>Malachite Kingfisher:</strong> Found perched on papyrus stems at lake edge. Tiny, intensely colored, and cooperative subjects for macro-telephoto work.</li>
    <li><strong>African Darter (Anhinga):</strong> Dries wings dramatically on papyrus branches — a unique "crucifixion" pose that photographs superbly.</li>
    <li><strong>Goliath Heron:</strong> Africa's largest heron stands motionless in shallows. Approach slowly for portrait shots against the green papyrus backdrop.</li>
    <li><strong>African Jacana:</strong> Walks on lily pads using enormous feet. The reflection compositions on still morning water are outstanding.</li>
    <li><strong>Hippo Mouth-Opening Behavior:</strong> Territorial yawning — displaying enormous tusks — is triggered when boats approach respectfully. Your captain knows exactly how to elicit this behavior safely.</li>
    <li><strong>Great Crested Grebe:</strong> Elegant water birds with elaborate head plumage, perfect for behavioral sequence photography.</li>
    <li><strong>Yellow-Billed Stork:</strong> Stunning pink, white, and yellow plumage. Feeds actively in the shallows — ideal for action photography.</li>
</ol>

<h3>Lens & Gear Recommendations</h3>
<ul>
    <li><strong>Primary Wildlife Lens:</strong> 100–500mm or 150–600mm telephoto zoom (Canon, Nikon, Sony, or Sigma variants). This covers everything from hippo pod wide shots to close kingfisher portraits.</li>
    <li><strong>Backup Lens:</strong> 24–70mm for landscape shots of the escarpment reflections and wide hippo pod compositions.</li>
    <li><strong>Camera Settings:</strong> Use Aperture Priority, ISO 400–800, Continuous AF tracking. In the golden hour, shutter speeds of 1/800s or faster prevent motion blur on flying birds.</li>
    <li><strong>Protection:</strong> Bring a waterproof camera bag or dry bag. Lake spray and unexpected rain squalls can soak unprotected equipment in minutes.</li>
</ul>

<h3>Book Your Photography Charter</h3>
<p>Contact Rafiki on WhatsApp at <strong>+254 701 215 295</strong> to book a dedicated photography charter. Mention you are a photographer and the captain will be briefed specifically to maximize your photographic access — moving slowly, holding positions, and orienting the boat for optimal light direction throughout your session.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 5. BIRTHDAY BOAT RIDE
    # ------------------------------------------------------------------ #
    {
        'title': 'Birthday Boat Ride Lake Naivasha Party Safari',
        'slug': 'birthday-boat-ride-lake-naivasha',
        'seo_title': 'Birthday Boat Ride Lake Naivasha | Group Party Safari 2026',
        'meta_description': 'Celebrate your birthday with an unforgettable boat ride on Lake Naivasha! Group hippo safari, cake on the water, music & Crescent Island. Book with Rafiki today.',
        'primary_keyword': 'birthday boat ride Lake Naivasha',
        'location': 'Lake Naivasha, Naivasha',
        'modifiers': 'birthday, party, celebration, group, cake, special occasion, friends',
        'content': """
<h2>The Most Epic Birthday Party in the Rift Valley</h2>

<p>Forget the crowded Nairobi restaurant or the noisy rooftop bar. The most original, most talked-about, most Instagram-worthy birthday celebration within 100 kilometers of Nairobi is a <strong>private birthday boat safari on Lake Naivasha</strong>. Imagine cutting your birthday cake while a pod of hippos grunts in the background, and a majestic African Fish Eagle screams overhead. That is a birthday story your friends will retell for the next twenty years.</p>

<h3>Why a Boat Birthday Party Works</h3>
<ul>
    <li><strong>Completely Unique:</strong> No other birthday celebration in Nairobi's saturated events scene competes with an open-water safari experience. It is 100% original, making your birthday truly memorable.</li>
    <li><strong>Perfect Group Size:</strong> One standard Rafiki boat comfortably accommodates groups of 6–7 people. For larger birthday groups of 14–20 friends, Rafiki deploys two boats that travel together as a convoy — creating a party fleet.</li>
    <li><strong>Spontaneous Joy:</strong> Wild animals are inherently unpredictable. A hippo suddenly surfacing two meters from the boat, or a fish eagle dramatically snatching a tilapia from the water right next to you, generates the kind of spontaneous, shared laughter that bonds friendship groups for life.</li>
</ul>

<h3>The Birthday Safari Package</h3>
<p>Rafiki works with you to personalize every detail of your birthday boat ride:</p>

<ol>
    <li><strong>Welcome at the Beach:</strong> Your captain greets the birthday group at Karagita Beach with personalized signage and ensures everyone is properly fitted with life jackets before a group photo.</li>
    <li><strong>The Safari:</strong> A 2-hour guided hippo and bird safari covers the lake's most spectacular locations. Your captain narrates and locates wildlife while you and your friends enjoy the ride.</li>
    <li><strong>Birthday Moment on the Water:</strong> At a pre-planned GPS coordinate — ideally with the volcanic escarpment or Crescent Island in the background — the captain slows the boat for the birthday cake cutting ceremony. Bring your own cake in a waterproof container, or coordinate with a local Naivasha bakery for delivery to the beach.</li>
    <li><strong>Post-Safari Tilapia Feast:</strong> Head straight from the boat to Karagita Beach's famous open-air fish kitchen for fresh, charcoal-grilled tilapia served with ugali — the ultimate group lakeside birthday feast.</li>
</ol>

<h3>Music and Celebration</h3>
<p>Rafiki allows Bluetooth speakers on private birthday charters. Bring your curated birthday playlist. At low volume, music enhances the experience without disturbing the wildlife observation. (Note: heavy subwoofer speakers are not permitted as vibrations disturb the lake ecosystem.)</p>

<h3>Book Your Birthday Safari</h3>
<p>Contact Rafiki on WhatsApp at <strong>+254 701 215 295</strong> at least 3 days before your preferred date. Mention it is a birthday celebration so the team can brief the captain and coordinate any special arrangements. Rafiki issues personalized booking confirmations that can be shared as birthday invitations on WhatsApp groups.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 6. PRIVATE BOAT CHARTER HIRE
    # ------------------------------------------------------------------ #
    {
        'title': 'Private Boat Hire Lake Naivasha Charter',
        'slug': 'private-boat-hire-lake-naivasha',
        'seo_title': 'Private Boat Hire Lake Naivasha | Charter Rates & Booking 2026',
        'meta_description': 'Hire a private boat on Lake Naivasha for your group. Transparent flat-rate charter pricing, certified captains, custom itineraries. Book directly with Rafiki — no broker commissions.',
        'primary_keyword': 'private boat hire Lake Naivasha',
        'location': 'Karagita Beach, Lake Naivasha',
        'modifiers': 'private charter, hire, exclusive, flat rate, custom itinerary, group',
        'content': """
<h2>Your Boat, Your Schedule, Your Safari</h2>

<p>A private boat charter on Lake Naivasha gives you complete control over your wildlife safari experience. Unlike shared group rides — where your itinerary is dictated by the majority vote of strangers — a private Rafiki charter means your certified captain works exclusively for your group. You decide where to go, how long to stay near the hippo pods, when to drift silently through the papyrus channels, and exactly when to turn back.</p>

<h3>Transparent Flat-Rate Charter Pricing</h3>
<p>Rafiki operates on a <strong>100% transparent flat-rate per-boat pricing model</strong>. There are no per-person charges, no hidden commission fees, no "peak season surcharges," and no negotiating with shoreline brokers. You pay one fixed rate per boat per hour, regardless of how many passengers you carry (up to the safety maximum).</p>

<ul>
    <li><strong>Standard 5-Person Open Fiberglass Safari Boat:</strong> Custom flat-rate quote provided directly — contact +254 701 215 295 for current rates.</li>
    <li><strong>Large 7-Person Capacity Boat:</strong> Ideal for families and small groups. Flat-rate pricing available on request.</li>
    <li><strong>Multi-Boat Fleet Hire:</strong> For groups exceeding 7 passengers, Rafiki deploys multiple boats simultaneously at a consolidated group rate.</li>
</ul>

<p><strong>Pro Tip:</strong> For a group of 4–7 people, a private charter almost always works out cheaper per person than paying individual "shared ride" rates at the beach — while giving you a dramatically better, fully personalized experience.</p>

<h3>Custom Itinerary Options</h3>
<p>When booking a private charter, specify your priorities and the captain will build your perfect route:</p>

<ul>
    <li><strong>Hippo Focus Route:</strong> Navigate directly to the main hippo pods in the southeastern lake basin. Best for first-time visitors and families with children. Duration: 1.5 hours.</li>
    <li><strong>Birding Specialist Route:</strong> Slow navigation through the papyrus channels and reed beds of the western lake shore, targeting specific bird species. Best at dawn. Duration: 2–3 hours.</li>
    <li><strong>Crescent Island Transfer:</strong> Direct crossing to Crescent Island game sanctuary for a walking safari with giraffes and zebras. Captain waits at the island dock and returns you to the mainland. Duration: 2.5 hours total.</li>
    <li><strong>Full Lake Circuit:</strong> A comprehensive 3-hour circuit covering hippo pools, Oloidien channel, Crescent Island approach, bird columns, and the open lake — the flagship Rafiki experience for returning visitors.</li>
    <li><strong>Sunset Golden Hour Charter:</strong> Departing at 4:30 PM, this 2-hour sunset charter follows the optimal light from the western channels to the open lake as the sun sets behind the Mau Escarpment.</li>
</ul>

<h3>What is Included in Every Private Charter</h3>
<ul>
    <li>Certified, experienced lake captain with 5+ years on Lake Naivasha</li>
    <li>Properly fitted life jackets for every passenger (including children)</li>
    <li>Fuel for the entire booked duration</li>
    <li>Expert wildlife commentary and species identification</li>
    <li>Secure vehicle parking assistance at Karagita Beach</li>
    <li>Broker-free, commission-free direct booking</li>
</ul>

<h3>How to Book Your Private Charter</h3>
<p>Booking is instant via WhatsApp at <strong>+254 701 215 295</strong>. Send your preferred date, departure time, group size, and any special requests (photography focus, birthday celebration, etc.). Rafiki will confirm availability, provide a flat-rate quote, and send you a GPS pin for the meeting point at Karagita Beach. No deposit is required for groups under 10 people — pay on arrival.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 7. HELL'S GATE COMBO TOUR
    # ------------------------------------------------------------------ #
    {
        'title': "Hell's Gate and Lake Naivasha Boat Ride Combo Tour",
        'slug': 'hells-gate-lake-naivasha-boat-ride-combo',
        'seo_title': "Hell's Gate + Lake Naivasha Boat Ride: The Ultimate Day Trip",
        'meta_description': "Combine Hell's Gate National Park cycling with a Lake Naivasha hippo boat safari. The ultimate Naivasha day trip from Nairobi — gorge hikes, cycling, wildlife & boat rides.",
        'primary_keyword': "Hell's Gate Lake Naivasha combo tour",
        'location': "Hell's Gate National Park, Lake Naivasha",
        'modifiers': 'cycling, gorge, hiking, combo, day trip, Nairobi, cycling safari',
        'content': """
<h2>Kenya's Most Action-Packed Day Trip</h2>

<p>If you have just one full day to spend in Naivasha, the <strong>Hell's Gate + Lake Naivasha Boat Ride combo</strong> is the single most rewarding, most diverse, and most memorable experience you can pack into 10 hours. You will cycle freely past herds of zebras and giraffes through a volcanic national park, hike through towering basalt gorges carved by ancient rivers, and then glide silently across Africa's most beautiful freshwater lake watching hippos and fish eagles — all before the sun sets behind the Rift Valley escarpment.</p>

<h3>The Perfect Day Itinerary</h3>

<h4>6:30 AM — Depart Nairobi (or Start at Your Naivasha Lodge)</h4>
<p>Leave Nairobi before the traffic builds. If you are already staying in Naivasha, begin your morning from your lodge. Grab breakfast en route — Kikopey's famous nyama choma joints or Gilgil's roadside mandazi stalls are popular stops.</p>

<h4>8:30 AM — Hell's Gate National Park: The Cycling Safari</h4>
<p>Hell's Gate is one of only two national parks in Kenya where visitors can cycle freely among wildlife without a guide vehicle. Rent bicycles at the park gate (KES 600/hour) and ride the 24-kilometer circuit loop through the park's interior.</p>
<ul>
    <li><strong>Wildlife Encounters:</strong> Zebras, giraffes, hartebeest, buffalo, and baboons are commonly seen directly from the cycling path. The animals are accustomed to cyclists and allow remarkably close approaches.</li>
    <li><strong>Fischer's Tower:</strong> A 25-meter volcanic plug that appears suddenly in the middle of the valley. It appeared in the opening sequence of the film "The Lion King."</li>
    <li><strong>The Gorge:</strong> A hidden 3-kilometer foot trail drops into a dramatic, cathedral-like basalt gorge carved by ancient geothermal hot springs. The walk through the gorge bottom — between towering vertical walls — is spectacular and requires 1.5 hours.</li>
</ul>

<h4>12:30 PM — Lunch Break</h4>
<p>Exit the park and drive 15 minutes to Karagita Beach. Enjoy fresh grilled tilapia from the local fish market — the perfect fuel for an afternoon on the water.</p>

<h4>2:00 PM — Lake Naivasha: Private Hippo Boat Safari</h4>
<p>Board your pre-booked Rafiki private boat charter at Karagita Beach for a 2-hour hippo and bird safari. The afternoon light, while stronger than morning, creates beautiful contrast shots of hippos against the volcanic crater lake background. Your Rafiki captain narrates the wildlife while you rest comfortably after the morning's exertions.</p>

<h4>4:30 PM — Optional Sunset Extension</h4>
<p>For the full experience, extend your boat charter to catch the golden sunset over the Mau Escarpment. The evening light at 5:00–6:00 PM transforms the lake into one of the most photographically stunning landscapes in East Africa.</p>

<h3>Logistics and Booking</h3>
<ul>
    <li><strong>Hell's Gate Entry Fees (2026):</strong> Non-resident adults: USD 26. Kenyan citizens: KES 215. Bicycle hire: KES 600/hour from the gate.</li>
    <li><strong>Boat Ride Booking:</strong> Pre-book your Rafiki boat charter to guarantee your afternoon slot. Walk-up bookings on busy weekends risk lengthy waits. Contact <strong>+254 701 215 295</strong> on WhatsApp.</li>
    <li><strong>Total Budget Estimate:</strong> Park entry + cycling + boat safari + tilapia lunch = approximately KES 8,000–12,000 per person for a fully private, premium experience.</li>
</ul>

<p>This combination delivers more wildlife diversity, physical activity, and natural beauty than almost any other single-day experience available within 100 kilometers of Nairobi.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 8. FISHING TOUR
    # ------------------------------------------------------------------ #
    {
        'title': 'Lake Naivasha Fishing Tour Tilapia and Bass',
        'slug': 'lake-naivasha-fishing-tour',
        'seo_title': 'Lake Naivasha Fishing Tour | Tilapia & Largemouth Bass Guide',
        'meta_description': 'Go fishing on Lake Naivasha! Target tilapia, largemouth bass & black bass. Private fishing charter with certified captain, rods & bait included. Book with Rafiki.',
        'primary_keyword': 'Lake Naivasha fishing tour',
        'location': 'Lake Naivasha',
        'modifiers': 'fishing, tilapia, bass, angling, freshwater fishing, charter, rods',
        'content': """
<h2>Kenya's Premier Freshwater Fishing Destination</h2>

<p>Lake Naivasha is one of East Africa's most productive and most diverse freshwater fishing lakes. The lake's pristine freshwater ecosystem, fed by underground springs and the Gilgil and Malewa rivers, supports extraordinary populations of target species that draw anglers from across Kenya, South Africa, and Europe every fishing season. A <strong>Rafiki private fishing charter</strong> puts you directly over the most productive fishing grounds with an experienced captain who knows exactly where the bass are holding and what the tilapia are feeding on today.</p>

<h3>Target Species on Lake Naivasha</h3>

<h4>Nile Tilapia (Oreochromis niloticus)</h4>
<p>The lake's most abundant and most sought-after species. Naivasha tilapia grow to impressive sizes — fish of 2–4 kg are common, and trophy specimens exceeding 5 kg are regularly landed in the papyrus channels. Tilapia are highly active feeders at dawn and dusk, making early morning and late afternoon the productive windows. Best method: light float fishing with bread paste or worm bait in the shallows.</p>

<h4>Largemouth Bass (Micropterus salmoides)</h4>
<p>Introduced to the lake decades ago, Naivasha's largemouth bass population has flourished in the lake's abundant papyrus-sheltered bays. Bass averaging 1–3 kg are common, with exceptional fish exceeding 4 kg possible in the deep channel edges. Best method: artificial lures (soft plastic worms, jerk shads, topwater poppers) worked along papyrus edges at first light.</p>

<h4>Black Bass</h4>
<p>Found in the deeper, open-water portions of the lake. Best targeted with deep-diving crankbaits and weighted drop-shot rigs in water between 3–6 meters deep.</p>

<h3>The Rafiki Fishing Charter Experience</h3>
<ul>
    <li><strong>Fishing Equipment:</strong> Rafiki's fishing charters include spinning rods, reels, and basic bait. Serious anglers are encouraged to bring their own specialist tackle for lure fishing.</li>
    <li><strong>Captain as Guide:</strong> Your Rafiki captain has fished the lake for years and understands seasonal fish movements, optimal tide times (the lake has minimal but measurable inflows), and the specific GPS hotspots for each species.</li>
    <li><strong>Catch and Keep:</strong> All tilapia caught are yours to keep. Your captain will assist with cleaning if required. Largemouth bass are recommended for catch-and-release to protect the growing sport fishery.</li>
    <li><strong>Combined Safari-Fishing:</strong> Book a "Fishing + Wildlife Combo" charter where the first hour targets hippos and birds for photography, and the second hour is dedicated anchored fishing in a productive bay — perfect for groups with mixed interests.</li>
</ul>

<h3>Best Times to Fish Lake Naivasha</h3>
<ul>
    <li><strong>Peak Feeding (All Species):</strong> 6:30 AM – 9:00 AM and 4:30 PM – 6:30 PM</li>
    <li><strong>Dry Season Fishing (Jan–Feb, Jul–Sep):</strong> Water clarity is highest. Surface lure fishing for bass is spectacular.</li>
    <li><strong>Rainy Season Fishing (Mar–May):</strong> Tilapia become highly active as inflow nutrients spike. Large tilapia move into shallow margins. Excellent float fishing conditions.</li>
</ul>

<h3>Book Your Fishing Charter</h3>
<p>Contact Rafiki on WhatsApp at <strong>+254 701 215 295</strong> to book a dedicated fishing charter. Specify whether you want a pure fishing session, a combined safari-fishing experience, or a group fishing competition for a team-building event. Rafiki will advise on optimal timing and required tackle.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 9. OLOIDIEN BAY
    # ------------------------------------------------------------------ #
    {
        'title': 'Oloidien Bay Lake Naivasha Boat Safari',
        'slug': 'oloidien-bay-lake-naivasha',
        'seo_title': 'Oloidien Bay Lake Naivasha: Hippos, Flamingos & Quiet Channels',
        'meta_description': 'Explore the quiet, flamingo-rich Oloidien Bay on Lake Naivasha. The lake\'s most biodiverse channel — hippos, flamingos & rare waterbirds. Book a Rafiki boat safari.',
        'primary_keyword': 'Oloidien Bay Lake Naivasha',
        'location': 'Oloidien Bay, Lake Naivasha',
        'modifiers': 'flamingos, hippos, waterbirds, quiet, channels, papyrus, biodiversity',
        'content': """
<h2>The Hidden Jewel of Lake Naivasha</h2>

<p>While most tourists focus on the main lake basin near Karagita Beach, Naivasha's most biologically extraordinary habitat is hidden in the quiet southwestern arm of the lake known as <strong>Oloidien Bay</strong>. Separated from the main lake by a narrow papyrus channel, Oloidien is a shallower, slightly more alkaline embayment that creates the perfect ecological conditions for species and experiences that are simply not available anywhere else on the lake.</p>

<h3>Why Oloidien is Ecologically Unique</h3>
<p>The slightly elevated mineral content of Oloidien Bay's water, combined with its shallower depth and more sheltered, wind-protected position, creates a microhabitat of extraordinary richness. The bay is one of the few locations on Lake Naivasha where all three of the following wildlife experiences can occur simultaneously:</p>

<ol>
    <li><strong>Lesser Flamingo Flocks:</strong> During good water conditions (particularly following rains that raise mineral concentrations), massive flamingo flocks of hundreds to thousands of birds visit Oloidien's shallower margins to feed on the blue-green algae that proliferates here. The pink mass of flamingos against the green papyrus and blue escarpment is among the most visually stunning sights in the entire Rift Valley.</li>
    <li><strong>Dense Hippo Pods:</strong> The sheltered bay and abundant waterborne vegetation make Oloidien one of the lake's primary hippo nursery areas. Large family pods, including mothers with newborn calves, are regularly observed here — an experience that is both scientifically fascinating and deeply moving.</li>
    <li><strong>Rare Waterbirds:</strong> The bay attracts species rarely seen on the main lake, including African Pygmy Goose, African Finfoot, and Papyrus Gonolek — sought-after tick species for serious Kenya birders completing their life lists.</li>
</ol>

<h3>The Oloidien Channel Passage</h3>
<p>Reaching Oloidien Bay requires navigating through a narrow papyrus channel connecting the two water bodies. This 800-meter passage through towering papyrus reeds is a wildlife experience in itself. With the motor idling at minimum speed, the boat glides silently through a cathedral of green reeds. Wattled Starlings, Long-tailed Cormorants, and Purple Herons erupt from the papyrus walls on both sides. It is an intimate, textural, sensory experience completely unlike the open-lake environment.</p>

<h3>Best Conditions for Visiting Oloidien</h3>
<ul>
    <li><strong>Flamingo Viewing:</strong> December through March following dry-season alkalinity concentration. Confirm flamingo presence with Rafiki captains before booking specifically for flamingos — their presence is seasonal and unpredictable.</li>
    <li><strong>Hippo Nursery:</strong> Year-round, but the bay is most productive for hippo calf sightings between March and July, following the main calving season.</li>
    <li><strong>Rare Bird Species:</strong> April and May during the long rains, when Afrotropical migrants arrive and resident species are at peak breeding activity.</li>
</ul>

<h3>Add Oloidien to Your Rafiki Charter</h3>
<p>The Oloidien Bay extension adds approximately 45 minutes to a standard Rafiki boat safari and is included in the "Full Lake Circuit" charter option. Contact Rafiki on WhatsApp at <strong>+254 701 215 295</strong> to specifically request the Oloidien route and ask about current flamingo conditions before your visit.</p>
""",
    },

    # ------------------------------------------------------------------ #
    # 10. HIPPO POINT AREA
    # ------------------------------------------------------------------ #
    {
        'title': 'Hippo Point Naivasha Boat Safari and Viewpoint',
        'slug': 'hippo-point-naivasha-boat-safari',
        'seo_title': 'Hippo Point Naivasha: Boat Safari, Viewpoint & Lodge Guide',
        'meta_description': 'Visit Hippo Point on Lake Naivasha for the ultimate hippo pod viewing. Boat safari access, Hippo Point Lodge, and the iconic sunset spot. Book a Rafiki boat ride.',
        'primary_keyword': 'Hippo Point Naivasha boat safari',
        'location': 'Hippo Point, South Lake Road, Naivasha',
        'modifiers': 'hippos, viewpoint, lodge, sunset, hippo pods, wildlife, South Lake Road',
        'content': """
<h2>The Most Famous Hippo Congregation on the Rift Valley</h2>

<p><strong>Hippo Point</strong> is the most iconic wildlife landmark on Lake Naivasha. Located on the southwestern shore of the lake at the end of the scenic South Lake Road, Hippo Point is a shallow, papyrus-fringed embayment where the lake's most accessible and most densely congregated hippo pods gather daily. For tourists, it is simultaneously a land-based viewpoint, a luxury lodge destination, and — most spectacularly — the starting point for the closest, most dramatic hippo boat safaris on the entire lake.</p>

<h3>The Hippo Pods of Hippo Point</h3>
<p>Lake Naivasha is home to over 1,500 individual hippos — one of the highest concentrations of hippopotamus per square kilometer of any freshwater lake in East Africa. The shallow, mud-bottomed coves around Hippo Point serve as daytime resting grounds for the lake's largest family pods, some containing 20–35 individual animals of all ages and sizes.</p>

<ul>
    <li><strong>Territorial Bulls:</strong> Large, scarred bulls maintain their territorial positions at the pod periphery. Their impressive open-mouthed threat display — revealing enormous ivory tusks — is triggered by rival males and provides extraordinary photographic opportunities.</li>
    <li><strong>Nursery Groups:</strong> Female hippos with calves of various ages cluster in the safer center of the pod. Calves nurse underwater for extended periods and are visible at the surface every few minutes.</li>
    <li><strong>Behavioral Range:</strong> The pods engage in yawning, grunting, sparring, and surface rolling behaviors throughout the day — each behavior creates unique photographic moments for patient observers.</li>
</ul>

<h3>The Boat Safari Advantage</h3>
<p>While the Hippo Point land viewpoint gives a distant overview of the pods, a <strong>Rafiki boat safari launching from Karagita Beach</strong> brings you into the lake's interior — allowing safe approaches to within 30–50 meters of the pods from multiple angles. From the water, you observe behaviors, sounds, and details that are completely invisible from the land viewpoint: the underwater movement of submerged hippos, the ear-flicking and barrel-rolling behaviors, and the extraordinary sight of a hippo walking along the lake bottom in 1.5 meters of clear water.</p>

<h3>Hippo Point Lodge: The Luxury Anchor</h3>
<p>The privately owned Hippo Point Lodge sits directly at the Hippo Point promontory. The lodge's iconic "Hippo Point Tower" — a converted Victorian water tower rising 17 meters above the lake surface — offers the highest, most dramatic panoramic views of the hippo pods, the lake, and the Mau and Aberdare escarpments in any direction. Day visitors can access the tower viewpoint for a fee. Lodge guests have exclusive dawn access to the tower — one of the most spectacular wildlife viewing experiences in Kenya.</p>

<h3>Book Your Hippo Safari</h3>
<p>Contact Rafiki Boat Rides on WhatsApp at <strong>+254 701 215 295</strong> to book a dedicated hippo-focused safari. Request the "Hippo Point Circuit" route, which maximizes time at the main pod locations while covering the western channel hippo nurseries for a comprehensive 2-hour hippopotamus experience.</p>
""",
    },
]


# ---------------------------------------------------------------------- #
# New internal links for Phase 9 pages
# ---------------------------------------------------------------------- #
new_links = [
    ('family boat ride Naivasha', '/seo/lake-naivasha-boat-ride-with-kids/'),
    ('kids boat ride Lake Naivasha', '/seo/lake-naivasha-boat-ride-with-kids/'),
    ('honeymoon boat ride Naivasha', '/seo/romantic-boat-ride-lake-naivasha-honeymoon/'),
    ('romantic sunset cruise Naivasha', '/seo/romantic-boat-ride-lake-naivasha-honeymoon/'),
    ('corporate team building Naivasha', '/seo/lake-naivasha-corporate-team-building/'),
    ('group boat safari Naivasha', '/seo/lake-naivasha-corporate-team-building/'),
    ('photography tour Lake Naivasha', '/seo/lake-naivasha-photography-tour/'),
    ('birding boat charter Naivasha', '/seo/lake-naivasha-photography-tour/'),
    ('birthday boat ride Naivasha', '/seo/birthday-boat-ride-lake-naivasha/'),
    ('private boat hire Naivasha', '/seo/private-boat-hire-lake-naivasha/'),
    ('private boat charter Lake Naivasha', '/seo/private-boat-hire-lake-naivasha/'),
    ("Hell's Gate boat ride combo", '/seo/hells-gate-lake-naivasha-boat-ride-combo/'),
    ('Hells Gate and Lake Naivasha', '/seo/hells-gate-lake-naivasha-boat-ride-combo/'),
    ('Lake Naivasha fishing tour', '/seo/lake-naivasha-fishing-tour/'),
    ('tilapia fishing Naivasha', '/seo/lake-naivasha-fishing-tour/'),
    ('Oloidien Bay Naivasha', '/seo/oloidien-bay-lake-naivasha/'),
    ('Oloidien flamingos', '/seo/oloidien-bay-lake-naivasha/'),
    ('Hippo Point Naivasha', '/seo/hippo-point-naivasha-boat-safari/'),
    ('Hippo Point boat safari', '/seo/hippo-point-naivasha-boat-safari/'),
]

print("=" * 60)
print("PHASE 9: pSEO LOCAL PAGES SEEDER")
print("=" * 60)

print("\n--- Creating/Updating Internal Links ---")
for kw, url in new_links:
    link, created = InternalLink.objects.update_or_create(
        keyword=kw,
        defaults={'url': url, 'is_active': True}
    )
    action = "NEW" if created else "UPD"
    print(f"  [{action}] '{kw}' -> {url}")

print(f"\n--- Creating/Updating {len(pages)} Local Pages ---")
created_count = 0
updated_count = 0
for data in pages:
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
    print(f"  [{action}] {page.title}")
    if created:
        created_count += 1
    else:
        updated_count += 1

print(f"\n{'=' * 60}")
print(f"PHASE 9 COMPLETE!")
print(f"  Local Pages Created: {created_count}")
print(f"  Local Pages Updated: {updated_count}")
print(f"  Internal Links Added: {len(new_links)}")
from seo.models import LocalPage
print(f"  Total Local Pages in DB: {LocalPage.objects.filter(is_active=True).count()}")
print(f"{'=' * 60}")
