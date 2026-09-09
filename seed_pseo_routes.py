"""
Programmatic SEO (pSEO) Matrix Generator for Origin-to-Destination Routes.
Creates 5 extremely detailed landing pages targeting high-intent logistical transit searches.
Run: python seed_pseo_routes.py
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import LocalPage

routes = [
    {
        'title': 'Nairobi to Lake Naivasha: The Complete Travel Guide',
        'slug': 'nairobi-to-lake-naivasha-drive-matatu-guide',
        'seo_title': 'How to Get From Nairobi to Lake Naivasha (2026 Guide)',
        'meta_description': 'The ultimate guide to traveling from Nairobi to Lake Naivasha. Driving times, A104 road conditions, Matatu prices, Uber costs, and the SGR train option.',
        'primary_keyword': 'Nairobi to Lake Naivasha',
        'location': 'Route from Nairobi',
        'modifiers': 'Matatu, SGR, Uber, Driving, Distance',
        'content': """
<h2>The Great Rift Valley Descent</h2>

<p>Traveling from the sprawling metropolis of Nairobi down to the serene waters of Lake Naivasha is one of the most classic, heavily trafficked tourist routes in East Africa. Because the lake is geographically close to the capital, it serves as the ultimate weekend getaway for locals and the perfect "first stop" for international tourists beginning a massive Kenyan safari.</p>

<p>Here is exactly how to navigate the 90-kilometer journey from Nairobi to Rafiki's <strong><a href="/boat-ride-at-lake-naivasha/">Lake Naivasha boat ride</a></strong> docks.</p>

<h2>1. Driving a Private Vehicle or Rental</h2>

<p>If you have rented a car or hired a private safari van, the drive is incredibly scenic but requires absolute concentration.</p>

<ul>
    <li><strong>The Distance:</strong> Roughly 90 kilometers from the Nairobi Central Business District (CBD) to the South Lake Road turn-off.</li>
    <li><strong>The Driving Time:</strong> Without traffic, the drive takes 1 hour and 45 minutes. With heavy Friday evening Nairobi traffic, it can take 3 to 4 hours. <strong>Always leave Nairobi before 6:30 AM or after 10:00 AM.</strong></li>
    <li><strong>The Route:</strong> You will take the A104 Highway (The Nairobi-Nakuru Highway). This is the main transit artery across East Africa. It is a massive, highly dangerous, single-lane highway dominated by 18-wheel cargo trucks driving to Uganda.</li>
    <li><strong>The Viewpoint:</strong> You must stop at the Kinangop Escarpment Viewpoint located roughly 45 minutes outside of Nairobi. It offers a colossal, panoramic view of the entire Rift Valley floor before you descend.</li>
</ul>

<h2>2. Taking a Public Matatu (The Budget Option)</h2>

<p>If you are a backpacker, taking a Matatu (a brightly painted, aggressively driven 14-seater public minibus) is the cheapest and most authentic way to travel.</p>

<ul>
    <li><strong>Where to Board:</strong> Take a Bolt or Uber to the "Nyamakima" or "River Road" stages in downtown Nairobi. Look for the massive yellow line of "Mololine" or "Naivasha North Rift" shuttles.</li>
    <li><strong>The Cost:</strong> The ticket costs exactly KES 300 to KES 400 ($2.50 to $3.50). </li>
    <li><strong>The Experience:</strong> Matatus do not leave on a schedule; they leave when they are perfectly full. The ride will be loud (massive sound systems), highly cramped, but incredibly fast. They will drop you in the center of Naivasha town.</li>
    <li><strong>The Final Leg:</strong> Once in Naivasha town, you must take a yellow taxi (KES 1,500) or a local Boda Boda motorcycle (KES 200) the final 15 kilometers down South Lake Road to Karagita beach for your <strong><a href="/tour-lake-naivasha/">Naivasha tour</a></strong>.</li>
</ul>

<h2>3. Taking an Uber or Bolt</h2>

<p>Yes, you can actually take an Uber directly from Nairobi to Lake Naivasha. It is the easiest, stress-free option for small groups.</p>
<ul>
    <li><strong>The Cost:</strong> Depending on surge pricing and rain, an Uber ChapChap (a small Suzuki Alto) will cost roughly KES 4,500 to KES 6,000 ($35 - $45). An Uber X (a larger sedan) will cost KES 6,000 to KES 8,000.</li>
    <li><strong>The Catch:</strong> Because Naivasha is outside the primary Nairobi operating zone, drivers cannot find a return fare. Many drivers will physically accept the ride on the app, then call you and demand you pay their return toll/fuel in cash before they pick you up. Agree on a flat fee of KES 7,000 via WhatsApp before getting in the car.</li>
</ul>

<h2>4. The SGR Train (The Standard Gauge Railway)</h2>

<p>Kenya's massive, multi-billion-dollar Chinese SGR train network technically connects from Nairobi to Naivasha/Suswa.</p>
<ul>
    <li>You can catch the sleek passenger train from the massive Syokimau terminal in Nairobi.</li>
    <li><strong>The Problem:</strong> The train does not go to the lake. It drops you at the massive "Mai Mahiu / Suswa" terminal, which is literally in the middle of a dusty, empty volcanic desert. You then have to hire an expensive taxi to drive you 40 minutes back to the lake to catch your <strong><a href="/sunset-cruises-naivasha/">sunset cruise</a></strong>. For tourists, driving is vastly superior to the train for this specific route.</li>
</ul>

<p>Regardless of how you physically arrive, the moment you step off the dusty highway and onto a floating Rafiki vessel for a flawless <strong><a href="/boat-safari-lake-naivasha/">hippo boat safari</a></strong>, the stress of the A104 highway instantly vanishes.</p>
        """
    },
    {
        'title': 'JKIA Airport to Lake Naivasha: Direct Transfer Guide',
        'slug': 'jkia-nairobi-airport-to-lake-naivasha-transfer',
        'seo_title': 'JKIA Airport to Lake Naivasha: Taxis, Shuttles & Drive Times',
        'meta_description': 'How to travel directly from Jomo Kenyatta International Airport (JKIA) to Lake Naivasha. Avoid Nairobi traffic, book direct shuttles, and start your safari instantly.',
        'primary_keyword': 'JKIA to Lake Naivasha',
        'location': 'Jomo Kenyatta Airport',
        'modifiers': 'Transfer, Taxi, Bypass, Shuttle, Direct',
        'content': """
<h2>Bypassing the Capital City</h2>

<p>For decades, international tourists arriving at Jomo Kenyatta International Airport (JKIA) after a brutal 14-hour flight from Europe or America had to endure a horrific 3-hour journey through grinding Nairobi city traffic just to reach the highway heading towards the Rift Valley.</p>

<p>Today, thanks to magnificent new Chinese-built infrastructure, you can land at JKIA, collect your bags, completely bypass Nairobi, and be physically sitting on a <strong><a href="/boat-ride-at-lake-naivasha/">Lake Naivasha boat ride</a></strong> drinking a cold beer in under 2.5 hours.</p>

<h2>The Magic of the Nairobi Expressway</h2>

<p>The game-changer for this route is the massive elevated toll road called the <strong>Nairobi Expressway</strong>. </p>

<p>The entrance to the Expressway is literally 400 meters outside the JKIA arrival terminal. By hiring a private transfer or a premium airport taxi, your driver will pay the small electronic toll and merge onto the elevated skyway. You will effectively fly over the entire city of Nairobi at 80 km/h, looking down at the legendary traffic jams below.</p>

<p>The Expressway dumps you directly onto the A104 Highway right at the escarpment base in exactly 20 minutes, cutting 2 hours off the transit time.</p>

<h2>Transfer Options from JKIA</h2>

<h3>1. Pre-Booked Safari Vans</h3>
<p>If you booked a structured <strong><a href="/tour-lake-naivasha/">Naivasha tour</a></strong> through a DMO (Destination Management Organization), your guide will meet you inside the Arrivals Hall holding a placard. You will load into an 8-seater customized Toyota Land Cruiser and immediately head for the Expressway. This is the safest and most comfortable method.</p>

<h3>2. The Airport Taxis (Yellow Cabs)</h3>
<p>There is a massive fleet of official, heavily regulated yellow taxis waiting outside JKIA. You do not need to pre-book them.</p>
<ul>
    <li>Walk up to the official dispatch desk just outside the sliding doors. Do not talk to the random touts shouting "Taxi, boss!"</li>
    <li>Request a direct flat-rate drop to "South Lake Road, Naivasha."</li>
    <li><strong>The Cost:</strong> Expect to pay exactly $80 to $100 USD (roughly KES 10,000 to 13,000). You must explicitly mandate that the driver uses the Expressway toll road.</li>
</ul>

<h3>3. Uber and Bolt from the Airport</h3>
<p>You can call a Bolt or Uber from JKIA to Naivasha.</p>
<ul>
    <li>They are not allowed to pick you up directly at the Arrivals curb. You must walk with your luggage to the massive concrete Parking Garage across the street.</li>
    <li>An Uber will cost roughly $50. However, the cars are usually very small (Suzuki Altos) and cannot fit two massive international suitcases. If you have heavy luggage, you must order an "Uber XL."</li>
</ul>

<h2>The Ideal Timing</h2>

<p>If your British Airways or KLM flight lands perfectly at 6:30 AM, you will clear customs by 7:30 AM. By utilizing the Expressway, you will arrive at our Rafiki docks on South Lake Road by exactly 10:00 AM. </p>
<p>Because you bypassed the city entirely, you can instantly begin your vacation with a peaceful morning <strong><a href="/boat-safari-lake-naivasha/">hippo boat safari</a></strong>, grab a fresh Tilapia lunch, check into your resort at 2:00 PM, and collapse into a massive, well-deserved sleep.</p>
        """
    },
    {
        'title': 'Nakuru to Lake Naivasha: The Inter-Lake Transit Guide',
        'slug': 'nakuru-to-lake-naivasha-drive-safari',
        'seo_title': 'How to Get From Nakuru to Lake Naivasha (Route Guide)',
        'meta_description': 'Traveling between the Great Rift Valley lakes. How to drive from Lake Nakuru National Park to Lake Naivasha, including distance, road conditions, and matatu options.',
        'primary_keyword': 'Nakuru to Lake Naivasha',
        'location': 'Route from Nakuru',
        'modifiers': 'Driving, Distance, Matatu, Lakes, A104',
        'content': """
<h2>Connecting the Two Jewels of the Rift</h2>

<p>If you are exploring the floor of the Great Rift Valley, you are almost guaranteed to be visiting both Lake Nakuru (famous for its rhinos and alkaline chemistry) and Lake Naivasha (famous for its massive hippo population and freshwater ecology).</p>

<p>The journey between these two heavy-hitting tourist destinations is incredibly fast, utterly painless, and completely devoid of the stressful escarpment traffic found on the Nairobi routes. Here is how to easily transit from the dusty plains of Nakuru to a serene <strong><a href="/boat-ride-at-lake-naivasha/">Lake Naivasha boat ride</a></strong>.</p>

<h2>The Route and Distance</h2>

<p>Lake Nakuru and Lake Naivasha are located on the exact same flat tectonic valley floor. You are literally just driving in a straight line southeast down the A104 highway.</p>

<ul>
    <li><strong>The Distance:</strong> 70 kilometers.</li>
    <li><strong>The Driving Time:</strong> Exactly 1 hour and 15 minutes, assuming you do not get stuck behind a massively overloaded truck climbing the small Gilgil hills.</li>
    <li><strong>The Road Conditions:</strong> The entire stretch is fully paved, multi-lane tarmac. It is phenomenally smooth compared to the roads inside the national parks.</li>
</ul>

<h2>Transit Method 1: The Fast Matatu</h2>

<p>Because Nakuru and Naivasha are both massive commercial hubs, there is a constant, highly aggressive battle between competing Matatu (public minibus) companies running this specific route.</p>

<ul>
    <li>Walk to the main Matatu stage in Nakuru Town. Look for shuttles marked either <strong>2NK Sacco</strong> or <strong>Mololine</strong>.</li>
    <li>The cost is shockingly cheap: roughly KES 250 ($2.00).</li>
    <li>The vehicles leave every 10 minutes. The journey is incredibly fast and efficient. They will drop you directly at the main Naivasha stage. From there, take a KES 200 motorcycle down South Lake Road to start your <strong><a href="/tour-lake-naivasha/">Naivasha tour</a></strong>.</li>
</ul>

<h2>Transit Method 2: The Self-Drive Safari</h2>

<p>If you have rented a car, leaving the Lanet Gate of Lake Nakuru National Park and pointing the nose towards Naivasha is a joy.</p>

<p><strong>The Mandatory Scenic Stops:</strong></p>
<ol>
    <li><strong>Kikopey (The Meat Stop):</strong> Roughly halfway into the journey, you will hit the small, dusty town of Kikopey. This is the undisputed "Nyama Choma" (roasted meat) capital of Kenya. Stop here, buy half a kilo of freshly roasted goat meat salted on butcher paper, and eat it by the side of the road before continuing.</li>
    <li><strong>Lake Elementaita Viewpoint:</strong> Just past Kikopey, the road rises slightly, giving you a massive panoramic view of the shallow, pink, flamingo-covered waters of Lake Elementaita. It is the perfect photographic interlude.</li>
</ol>

<h2>Timing the Arrival</h2>

<p>If you do a final 6:00 AM game drive in Nakuru to see the rhinos, leave the park by 11:00 AM. You will comfortably arrive in Naivasha just in time for a massive lunch. By 4:00 PM, the harsh overhead sun will drop, the thermal winds will die down, and you can seamlessly transition into a majestic, golden hour <strong><a href="/sunset-cruises-naivasha/">sunset cruise</a></strong> right on the water.</p>
        """
    },
    {
        'title': 'The Maasai Mara to Lake Naivasha Safari Route',
        'slug': 'maasai-mara-to-lake-naivasha-drive',
        'seo_title': 'Maasai Mara to Lake Naivasha: The Decompression Route',
        'meta_description': 'How to drive from the Maasai Mara directly to Lake Naivasha. Turn off the dusty Narok highway and decompress with a hippo boat safari on the lake.',
        'primary_keyword': 'Maasai Mara to Lake Naivasha',
        'location': 'Route from Maasai Mara',
        'modifiers': 'Narok, Mai Mahiu, Distance, Driving, Safari Route',
        'content': """
<h2>The Ultimate Safari Decompression</h2>

<p>Spending four days bouncing violently inside a 4x4 Land Cruiser across the rutted, dusty, predator-filled plains of the Maasai Mara is incredibly exhilarating, but physically exhausting. You will be covered in fine volcanic dust and tired from 5:00 AM wake-up calls.</p>

<p>Instead of driving 6 grueling hours straight back to Nairobi's heavy city traffic, the smartest tourists execute a "Decompression Stop." They drive from the Mara straight into the cool, silent waters of a <strong><a href="/boat-ride-at-lake-naivasha/">Lake Naivasha boat ride</a></strong>.</p>

<h2>The Route: From Dust to Water</h2>

<p>Driving from the Sekenani Gate of the Maasai Mara to Lake Naivasha requires navigating the famous Narok Highway.</p>

<ul>
    <li><strong>The Distance:</strong> Roughly 230 Kilometers.</li>
    <li><strong>The Driving Time:</strong> Extremely variable depending on rain and the specific Mara gate you exit from, but expect 4.5 to 5.5 hours of hard driving.</li>
    <li><strong>The Topography:</strong> You will drive straight north from the Mara on newly paved roads to the massive agricultural town of Narok (the wheat capital of Kenya). From Narok, you drive east towards Nairobi. However, you will NOT climb the massive escarpment. Instead, you will take the left turn at the dusty junction town of <strong>Mai Mahiu</strong>, driving straight up the valley floor to Naivasha.</li>
</ul>

<h2>Why You Must Stop in Naivasha</h2>

<p>Routing your safari directly from the Mara to Rafiki's docks is the ultimate physiological reset.</p>

<ol>
    <li><strong>Physical Freedom:</strong> In the Mara, you are strictly confined to your vehicle due to lions. When you arrive in Naivasha, you can finally walk. You can hike the gorges of Hell's Gate or walk physically among the giraffes on a guided <strong><a href="/tour-lake-naivasha/">Naivasha tour</a></strong> of Crescent Island.</li>
    <li><strong>Silence:</strong> Safari vans are incredibly loud. A specialized Rafiki <strong><a href="/boat-safari-lake-naivasha/">hippo boat safari</a></strong> uses quiet outboard motors. Gliding over the glassy water, listening only to the haunting call of the African Fish Eagle, is the perfect antidote to the chaotic growl of Land Cruiser engines.</li>
    <li><strong>The Dust Washer:</strong> The air over the lake is deeply humid, intensely cool, and entirely free of the harsh, granular dust that coats everything in the savannah.</li>
</ol>

<h2>Timing the Drive</h2>

<p>Depart your luxury tented camp in the Mara after an early morning breakfast at 8:00 AM. Stop at the massive modern gas stations in Narok at 11:30 AM for a bathroom break and strong Kenyan coffee.</p>

<p>By 1:30 PM, you will pull into the lush, green lawns of your Naivasha resort. Shower the dust off immediately, eat a fresh tilapia lunch by the water, and walk down to Rafiki's dock at 5:00 PM for the ultimate, relaxing <strong><a href="/sunset-cruises-naivasha/">sunset cruise</a></strong>. This is how the professionals end a Kenyan safari.</p>
        """
    },
    {
        'title': 'Mombasa to Lake Naivasha: From the Ocean to the Rift',
        'slug': 'mombasa-to-lake-naivasha-train-flight-guide',
        'seo_title': 'Mombasa to Lake Naivasha: SGR Train and Flight Options',
        'meta_description': 'The ultimate guide to traveling from the white sands of Mombasa and Diani to the hippos of Lake Naivasha. Compare the SGR Madaraka Express vs local flights.',
        'primary_keyword': 'Mombasa to Lake Naivasha',
        'location': 'Route from Mombasa',
        'modifiers': 'SGR, Train, Flight, Drive, Diani',
        'content': """
<h2>Swapping the Ocean for the Lake</h2>

<p>Kenya is famous for inventing the "Bush and Beach" itinerary: spending a week on safari in the interior, followed by a week relaxing on the searing hot white sands of Diani Beach or Mombasa. </p>

<p>However, if you are reversing the trip—moving from the humid, 35°C coastal ocean up into the cool, 1,884-meter altitude of the Great Rift Valley for a <strong><a href="/boat-ride-at-lake-naivasha/">Lake Naivasha boat ride</a></strong>—you are undertaking a massive logistical leap. The distance is roughly 580 kilometers. You effectively have two options: The Sky or The Rails.</p>

<h2>Option 1: The Fast Route (Flying)</h2>

<p>If you value time above all else, flying from the Indian Ocean to the Rift Valley is incredibly seamless.</p>

<ul>
    <li><strong>The Airports:</strong> Book a local low-cost carrier (JamboJet, SafariLink, or Kenya Airways) from Mombasa (MBA) or Ukunda/Diani (UKA) directly to Jomo Kenyatta International Airport (JKIA) in Nairobi.</li>
    <li><strong>The Flight Time:</strong> Exactly 1 hour. A ticket booked in advance costs roughly $50 to $80.</li>
    <li><strong>The Ground Transfer:</strong> As detailed in our JKIA transfer guide, once you land in Nairobi, hire an airport taxi to jump immediately onto the Nairobi Expressway. You will bypass the city entirely and arrive at the lake exactly 2.5 hours after touching down. </li>
    <li><strong>Total Transit Time:</strong> Less than 4.5 hours from the beach to a <strong><a href="/tour-lake-naivasha/">Naivasha tour</a></strong>.</li>
</ul>

<h2>Option 2: The Scenic Route (The SGR Train)</h2>

<p>If you want to view the massive, sweeping topography of Kenya slowly, you must take the Chinese-built Standard Gauge Railway (The Madaraka Express).</p>

<ul>
    <li><strong>The Train:</strong> Board the 8:00 AM passenger train at the massive Mombasa Terminus. The train is heavily air-conditioned, impeccably clean, and serves cold beers in the dining car.</li>
    <li><strong>The Views:</strong> The train slices directly through the middle of Tsavo National Park. You will physically see huge herds of red elephants and giraffes from your train window while traveling at 120 km/h.</li>
    <li><strong>The Connection:</strong> The train arrives at the Nairobi Syokimau Terminus at exactly 2:00 PM. Here, you have a crucial choice. You can either hire an Uber to drive you the remaining 2 hours to Naivasha via the highway, OR you can switch onto the "Phase 2" SGR link that goes specifically from Nairobi to Suswa (Naivasha).</li>
    <li><strong>Rafiki's Advice:</strong> Do not take the Phase 2 train to Suswa. The Suswa station is located in an empty, dust-blown desert 40 minutes away from the lake edge. Arrive in Nairobi at 2:00 PM by train, hire a taxi, and you will comfortably make it to Karagita beach just in time for a phenomenal <strong><a href="/sunset-cruises-naivasha/">sunset cruise</a></strong> through the hippo pools.</li>
</ul>

<p>Moving from the blinding humidity of the Indian Ocean to the crisp, eagle-filled skies of a Rafiki <strong><a href="/boat-safari-lake-naivasha/">hippo boat safari</a></strong> is the ultimate geographical transition.</p>
        """
    }
]

print("--- Seeding the Origin-to-Destination pSEO Matrix ---")
for data in routes:
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
        }
    )
    action = "CREATED" if created else "UPDATED"
    print(f"  [{action}] {page.title}")

print(f"\nSUCCESS! 5 Massive Logistical Transit Routes generated.")
print(f"These pages will automatically cross-link to your booking endpoints using the Phase 3 linking engine.")
