"""Bulk FAQ and Local Page seeder - 50 FAQs + 15 local pages. Run: python seed_faqs_pages.py"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()
from seo.models import FAQ, LocalPage, InternalLink

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

def LP(title, slug, seo, meta, kw, loc, mods, content):
    page, created = LocalPage.objects.update_or_create(slug=slug, defaults={
        'title': title, 'seo_title': seo, 'meta_description': meta,
        'primary_keyword': kw, 'location': loc, 'modifiers': mods,
        'content': content.strip(), 'is_active': True, 'allow_indexing': True})
    print(f"  [{'NEW' if created else 'UPD'}] {title}")

print("--- Creating 50 FAQs ---")

faqs = [
    ("How much does a boat ride in Naivasha cost?",
     "<p>Boat ride prices start from <strong>KES 1,000 per person per hour</strong> for group rides. Private charters, sunset cruises, and Crescent Island transfers are priced separately. We accept cash (KES/USD), M-Pesa, and bank transfers. WhatsApp +254 701 215 295 for exact pricing.</p>",
     "Prices start from KES 1,000 per person per hour. Private charters vary. We accept cash, M-Pesa, and bank transfers.", "pricing", 1),
    ("What is the best time for a boat ride at Lake Naivasha?",
     "<p>Early morning (6:30-9:00 AM) for calm waters and active wildlife. Late afternoon (3:00-6:30 PM) for stunning sunset views. We operate daily <strong>6:30 AM to 6:30 PM</strong>.</p>",
     "Early morning (6:30-9AM) for wildlife, late afternoon (3-6:30PM) for sunsets. Open daily 6:30AM-6:30PM.", "timing", 2),
    ("How do I get to Lake Naivasha from Nairobi?",
     "<p>Lake Naivasha is <strong>90 km from Nairobi</strong> (1.5-hour drive) via the Nairobi-Nakuru Highway (A104). Drive, take a matatu, or hire a taxi. Head to <strong>Public Beach, Karagita</strong>.</p>",
     "1.5 hours from Nairobi via Nairobi-Nakuru Highway. Our launch point is at Public Beach, Karagita.", "location", 3),
    ("Can I see hippos on a Lake Naivasha boat ride?",
     "<p>Yes! Hippo sightings are <strong>virtually guaranteed</strong> on every ride. Lake Naivasha has one of Kenya's largest hippo populations and our guides know exactly where they gather.</p>",
     "Yes! Hippos are virtually guaranteed. The lake has one of Kenya's largest hippo populations.", "wildlife", 4),
    ("What animals can I see at Crescent Island?",
     "<p>Walk freely among <strong>giraffes, zebras, wildebeest, waterbuck, elands, and impalas</strong>. The boat transfer also includes hippo and bird watching. Over 100 bird species on the island.</p>",
     "Giraffes, zebras, wildebeest, waterbuck, elands, impalas, and 100+ bird species.", "wildlife", 5),
    ("Are boat rides in Naivasha safe for children?",
     "<p>Absolutely! We provide <strong>life jackets in all sizes</strong> including children's. Our boats are well-maintained and captains prioritize safety. Private charters recommended for families with kids under 5.</p>",
     "Yes, very safe. Life jackets in all sizes, experienced captains, well-maintained boats.", "safety", 6),
    ("Do you offer boat rides near me in Naivasha?",
     "<p>We operate from <strong>Public Beach, Lake, Karagita</strong> - the main boat launch. Open daily 6:30 AM-6:30 PM. WhatsApp +254 701 215 295 or walk in.</p>",
     "We're at Public Beach, Karagita. Open daily 6:30AM-6:30PM. Walk-ins welcome.", "location", 7),
    ("What is the difference between a boat ride and boat safari?",
     "<p>A <strong>boat ride</strong> is a scenic cruise; a <strong>boat safari</strong> focuses on wildlife. At Rafiki, every ride includes wildlife spotting. We also offer dedicated hippo and bird safaris.</p>",
     "Boat ride = scenic cruise. Boat safari = wildlife focus. Every Rafiki ride includes both.", "booking", 8),
    ("Can I book a boat ride for a birthday or event?",
     "<p>Yes! We offer <strong>private charters</strong> for birthdays, anniversaries, proposals, and corporate events. Customize with champagne, music, and photography. Book 24 hours ahead.</p>",
     "Yes! Private charters for any event. Can add champagne, music, photography.", "booking", 9),
    ("What should I wear for a boat ride in Naivasha?",
     "<p>Comfortable layered clothing, hat, sunglasses, sunscreen (SPF 30+), closed-toe shoes, light waterproof jacket, and insect repellent. We provide life jackets.</p>",
     "Comfortable layers, hat, sunglasses, sunscreen, closed shoes. We provide life jackets.", "preparation", 10),
    ("How long is a typical boat ride on Lake Naivasha?",
     "<p>Standard ride: <strong>1 hour</strong>. Crescent Island tour: 2-3 hours. Sunset cruise: 1.5-2 hours. Full-day package: 5-7 hours. All customizable.</p>",
     "Standard: 1 hour. Crescent Island: 2-3 hours. Sunset: 1.5-2 hours. Full-day: 5-7 hours.", "timing", 11),
    ("Do you offer private boat rides in Naivasha?",
     "<p>Yes! Private charters give you a <strong>dedicated boat and guide</strong>. Perfect for couples, families, photographers, and groups wanting an exclusive experience.</p>",
     "Yes - dedicated boat and guide for your group only. Great for couples, families, events.", "booking", 12),
    ("What wildlife can I see during a Lake Naivasha boat ride?",
     "<p>Hippos, African Fish Eagles, pelicans, cormorants, kingfishers, herons, monitor lizards, and 400+ bird species. Crescent Island adds giraffes, zebras, and wildebeest.</p>",
     "Hippos, Fish Eagles, pelicans, 400+ bird species. Plus giraffes and zebras at Crescent Island.", "wildlife", 13),
    ("Do you offer sunset cruises on Lake Naivasha?",
     "<p>Yes! Our <strong>sunset cruises</strong> (4:00-6:30 PM) are our most romantic experience. Golden hour light, quiet channels, champagne available on request.</p>",
     "Yes! Sunset cruises run 4-6:30PM. Golden hour views, quiet channels, champagne on request.", "booking", 14),
    ("Is it safe to go on a boat ride at Lake Naivasha?",
     "<p>Very safe. <strong>Life jackets for all</strong>, licensed captains with 10+ years experience, regularly inspected boats, safe distances from hippos. Zero incidents in deep local experience.</p>",
     "Very safe. Life jackets, licensed captains, inspected boats, zero incidents in deep local experience.", "safety", 15),
    ("What is the best time for a boat ride on Lake Naivasha?",
     "<p>Morning (6:30-9 AM) for active wildlife and photography light. Afternoon (3-6:30 PM) for sunset views. Midday is warmest but less wildlife activity.</p>",
     "Morning for wildlife, afternoon for sunsets. Midday is warmest with less wildlife.", "timing", 16),
    ("What should I bring for a Lake Naivasha boat ride?",
     "<p>Camera, sunscreen, hat, sunglasses, insect repellent, light jacket, water bottle, binoculars (optional). We provide life jackets and guides.</p>",
     "Camera, sunscreen, hat, sunglasses, insect repellent, water. We provide life jackets.", "preparation", 17),
    ("How do I book a boat ride with Rafiki?",
     "<p>WhatsApp us at <strong>+254 701 215 295</strong> with your preferred date, time, group size, and activity. We'll confirm availability instantly. Walk-ins also welcome at Public Beach.</p>",
     "WhatsApp +254 701 215 295. Share date, time, group size, activity. Walk-ins welcome too.", "booking", 18),
    ("What types of boat rides do you offer on Lake Naivasha?",
     "<p>Standard hippo safari, Crescent Island transfer + walking safari, sunset cruise, photography safari, bird watching tour, fishing expedition, and private charters.</p>",
     "Hippo safari, Crescent Island, sunset cruise, photography, bird watching, fishing, private charters.", "booking", 19),
    ("How far is Lake Naivasha from Nairobi?",
     "<p><strong>90 km</strong> from Nairobi CBD - about 1.5 hours by car via the Nairobi-Nakuru Highway. The closest major lake to Nairobi.</p>",
     "90 km from Nairobi - about 1.5 hours drive on the Nairobi-Nakuru Highway.", "location", 20),
    ("Can I swim in Lake Naivasha?",
     "<p><strong>No</strong> - swimming is not recommended due to hippos, bilharzia risk, and the lake's ecosystem. Enjoy the water safely from our boats instead, or visit Olkaria hot springs for swimming.</p>",
     "No - not safe due to hippos and bilharzia. Enjoy from boats instead. Olkaria hot springs have safe swimming.", "safety", 21),
    ("What is the best month to visit Lake Naivasha?",
     "<p>January-February and June-October are dry seasons with clearest skies. However, the lake is beautiful year-round. Rainy months (March-May) bring more birds and lush scenery.</p>",
     "Jan-Feb and Jun-Oct are driest. But it's great year-round. Rain brings more birds and green scenery.", "timing", 22),
    ("Do I need to book in advance for a boat ride?",
     "<p>Walk-ins welcome on weekdays. <strong>Weekends and holidays</strong> - booking ahead recommended to guarantee your spot. Special events need 24-hour advance booking.</p>",
     "Walk-ins OK on weekdays. Book ahead for weekends/holidays. Events need 24-hour notice.", "booking", 23),
    ("Are there restaurants at Lake Naivasha?",
     "<p>Yes! Fresh grilled tilapia and other local dishes are available at <strong>Public Beach, Karagita</strong>. Several lakeside restaurants and lodges also serve meals nearby.</p>",
     "Yes - fresh tilapia at Public Beach, plus several lakeside restaurants and lodges nearby.", "amenities", 24),
    ("Can I bring food and drinks on the boat?",
     "<p>Yes! You're welcome to bring snacks, water, and beverages. For sunset cruises, we can arrange champagne and light refreshments on request.</p>",
     "Yes, bring snacks and drinks. We can also arrange champagne for sunset cruises.", "preparation", 25),
    ("What is Crescent Island?",
     "<p>A private wildlife sanctuary on Lake Naivasha where you can <strong>walk freely among giraffes, zebras, and wildebeest</strong>. Access is by boat from Public Beach. Famous filming location for 'Out of Africa.'</p>",
     "A wildlife sanctuary where you walk among giraffes and zebras. Access by boat. Filming location for Out of Africa.", "destination", 26),
    ("How deep is Lake Naivasha?",
     "<p>Average depth is <strong>6 meters</strong>, deepest point about 30 meters in Crescent Island crater. The lake is shallow enough for papyrus to grow along the shores but deep enough for hippos.</p>",
     "Average 6m deep, deepest 30m near Crescent Island. Shallow enough for papyrus, deep enough for hippos.", "general", 27),
    ("Do you provide life jackets?",
     "<p><strong>Yes - mandatory for all passengers</strong>. We provide life jackets in adult, child, and infant sizes. Safety is our top priority.</p>",
     "Yes, mandatory for everyone. Adult, child, and infant sizes available.", "safety", 28),
    ("Is Lake Naivasha a national park?",
     "<p><strong>No</strong> - Lake Naivasha is not a national park, so there's no park entry fee. This makes boat rides very affordable compared to traditional safari parks.</p>",
     "No - no park entry fee needed. This makes boat rides more affordable than park safaris.", "general", 29),
    ("Can I see flamingos at Lake Naivasha?",
     "<p>Occasionally, but flamingos are more common at <strong>Lake Nakuru and Lake Bogoria</strong>. Lake Naivasha's specialty is hippos, Fish Eagles, and 400+ other bird species.</p>",
     "Occasionally, but hippos and Fish Eagles are the main attractions. Flamingos are better at Lake Nakuru.", "wildlife", 30),
    ("What is the elevation of Lake Naivasha?",
     "<p><strong>1,884 meters</strong> above sea level. This gives Naivasha a pleasant, temperate climate - warm days (25-28C) and cool evenings - perfect for outdoor activities.</p>",
     "1,884m above sea level. Pleasant climate - warm days (25-28C) and cool evenings.", "general", 31),
    ("Do you accept M-Pesa payments?",
     "<p><strong>Yes!</strong> We accept M-Pesa, cash (KES/USD), and bank transfers. Payment is made before or upon boarding.</p>",
     "Yes! M-Pesa, cash (KES/USD), and bank transfers accepted.", "pricing", 32),
    ("How many people can fit on one boat?",
     "<p>Our boats accommodate <strong>2-12 passengers</strong> depending on the vessel. For larger groups, we coordinate multiple boats. Private charters available for any size.</p>",
     "2-12 people per boat. Multiple boats for larger groups. Private charters for any size.", "booking", 33),
    ("Is there parking at Public Beach?",
     "<p><strong>Yes</strong> - ample parking available at Public Beach, Karagita. The area is safe and monitored. Parking is free or minimal charge.</p>",
     "Yes, ample parking at Public Beach, Karagita. Safe and monitored.", "amenities", 34),
    ("Do you offer photography tours?",
     "<p>Yes! Our <strong>photography safaris</strong> are guided by experienced spotters who know the best angles, lighting, and wildlife locations. Slower pace, optimal positioning for shots.</p>",
     "Yes! Dedicated photography safaris with expert wildlife guides. Slow pace, optimal positioning.", "booking", 35),
    ("What happens if it rains during my boat ride?",
     "<p>Light rain usually doesn't affect the ride. For <strong>heavy storms, we reschedule at no cost</strong>. Morning rides are usually dry even during rainy season.</p>",
     "Light rain is fine. Heavy storms = free reschedule. Mornings usually dry even in rainy season.", "safety", 36),
    ("Can I see the sunrise from the boat?",
     "<p>Yes! Our <strong>earliest rides start at 6:30 AM</strong>, perfect for catching the sunrise over the Aberdare Mountains reflecting on the lake. Incredible photography opportunity.</p>",
     "Yes! 6:30 AM rides catch sunrise over the Aberdares. Amazing photography opportunity.", "timing", 37),
    ("Is Lake Naivasha good for bird watching?",
     "<p>Exceptional! Lake Naivasha is a designated <strong>Important Bird Area (IBA)</strong> with 400+ species. Our boat gives you a floating bird hide. Best birding: early morning.</p>",
     "Exceptional - 400+ species, designated IBA. Our boats are floating bird hides. Best in early morning.", "wildlife", 38),
    ("Do you offer student discounts?",
     "<p>Yes! We offer <strong>special rates for students and school groups</strong>. Educational ecology tours available with lesson plans aligned to the curriculum. Contact us for school pricing.</p>",
     "Yes! Special rates for students and schools. Educational tours available with lesson plans.", "pricing", 39),
    ("What is the water temperature of Lake Naivasha?",
     "<p>The lake surface temperature averages <strong>20-25 degrees Celsius</strong> year-round. Comfortable for the hippos but remember - no swimming recommended!</p>",
     "Surface temperature 20-25C year-round. Comfortable for hippos but no swimming recommended.", "general", 40),
    ("How do I get from my hotel to the boat launch?",
     "<p>Most Naivasha hotels and lodges can arrange transport to <strong>Public Beach, Karagita</strong>. It's 5-15 minutes from most accommodations. We can also help coordinate pickup.</p>",
     "Most hotels arrange transport. Public Beach is 5-15 min from most Naivasha accommodations.", "location", 41),
    ("Are there toilets at Public Beach?",
     "<p>Yes, toilet facilities are available at Public Beach. There are also restaurants where you can use facilities. We recommend using them before your boat ride.</p>",
     "Yes, toilets available at Public Beach. Also at nearby restaurants. Use before your ride.", "amenities", 42),
    ("Can I bring my pet on the boat?",
     "<p>We generally <strong>advise against bringing pets</strong> as they may get stressed by wildlife encounters (especially hippos). Service animals are welcome with advance notice.</p>",
     "Not recommended due to wildlife encounters. Service animals welcome with advance notice.", "preparation", 43),
    ("What is the history of Lake Naivasha?",
     "<p>Lake Naivasha has a rich history from <strong>Maasai pastoralists</strong> ('Nai-posha' meaning rough water) to colonial settlers and modern tourism. It's Kenya's highest-altitude major lake at 1,884m.</p>",
     "Named by Maasai ('Nai-posha' = rough water). Kenya's highest major lake at 1,884m. Rich colonial and tourism history.", "general", 44),
    ("Do you offer overnight camping by the lake?",
     "<p>We don't offer camping directly, but several <strong>campsites and lodges</strong> are located along the lake shore. We can recommend options for all budgets. Combine with early morning boat rides!</p>",
     "We don't do camping but can recommend lakeside campsites and lodges for all budgets.", "amenities", 45),
    ("What makes Rafiki different from other boat operators?",
     "<p><strong>guest-first reputation, verified guest feedback, deep local experience, woman-owned</strong>. We focus on quality over quantity - smaller groups, personal attention, and deep local knowledge.</p>",
     "guest-first reputation, verified guest feedback, deep local experience, woman-owned. Quality focus, small groups, local expertise.", "booking", 46),
    ("Can I tip my boat guide?",
     "<p>Tips are <strong>appreciated but not required</strong>. If your guide made your experience special, a tip of KES 200-500 is a kind gesture. It goes directly to the guide.</p>",
     "Appreciated but not required. KES 200-500 is a kind gesture that goes directly to your guide.", "pricing", 47),
    ("Is Lake Naivasha affected by drought?",
     "<p>Lake Naivasha water levels fluctuate naturally. We adapt our routes accordingly. <strong>Boat rides operate year-round</strong> regardless of water level changes.</p>",
     "Water levels fluctuate naturally but boat rides operate year-round. Routes adapt to conditions.", "general", 48),
    ("How do I leave a Google review for Rafiki?",
     "<p>Search '<strong>Rafiki Boat Rides Naivasha</strong>' on Google Maps, click our listing, and tap 'Write a review.' We read and respond to every review! Your feedback helps us improve.</p>",
     "Search 'Rafiki Boat Rides Naivasha' on Google Maps, click our listing, tap 'Write a review.'", "general", 49),
    ("Do you offer combo packages with other attractions?",
     "<p>Yes! We offer <strong>combo packages</strong> with Crescent Island, Hell's Gate, Elsamere Conservation Centre, and Mt. Longonot. Full-day and multi-day packages available.</p>",
     "Yes! Combos with Crescent Island, Hell's Gate, Elsamere, Mt. Longonot. Full-day and multi-day.", "booking", 50),
]

for q, a, plain, intent, order in faqs:
    F(q, a, plain, intent, order)

# Fix any remaining Njovic references
for faq in FAQ.objects.filter(question__icontains='Njovic'):
    faq.question = faq.question.replace('Njovic Boats', 'Rafiki').replace('Njovic', 'Rafiki')
    faq.answer = faq.answer.replace('Njovic Boats', 'Rafiki Boat Rides').replace('Njovic', 'Rafiki')
    faq.save()
    print(f"  [FIXED] {faq.question}")

print(f"\n--- Creating Local Pages ---")

LP("Boat Rides Naivasha",
   "boat-rides-naivasha",
   "Boat Rides Naivasha | Best Lake Naivasha Boat Tours - Rafiki",
   "Book the best boat rides in Naivasha with Rafiki. Hippo safaris, sunset cruises, Crescent Island tours. friendly, deep local experience.",
   "boat rides naivasha", "Naivasha, Lake Naivasha", "boat rides, naivasha, lake naivasha, tours",
   """<h2>Boat Rides Naivasha - Your Ultimate Lake Experience</h2>
<p><strong>Boat rides in Naivasha</strong> are the highlight of any visit to Lake Naivasha. At Rafiki Boat Rides, we offer the most trusted and highly-rated boat ride experience on the lake.</p>
<h3>Our Boat Rides</h3><ul><li>Hippo & bird safari (1 hour)</li><li>Crescent Island transfer + walking safari (2-3 hours)</li><li>Sunset cruise (1.5-2 hours)</li><li>Photography safari (2 hours)</li><li>Private charter (custom)</li></ul>
<h3>Why Choose Rafiki?</h3><p>guest-first reputation, verified guest feedback, deep local lake knowledge, locally owned and woman-led.</p>
<h3>Pricing</h3><p>From KES 1,000/person/hour. Group discounts for 10+.</p>
<h3>Hours & Location</h3><p>Daily 6:30 AM - 6:30 PM at Public Beach, Karagita, Naivasha.</p>
<p>Book: WhatsApp +254 701 215 295</p>""")

LP("Lake Naivasha Beach - Public Beach Karagita",
   "lake-naivasha-beach",
   "Lake Naivasha Beach | Public Beach Karagita - Boat Launch Point",
   "Visit Lake Naivasha Beach at Public Beach, Karagita. Main launch point for boat rides, fresh fish, views. Directions and info.",
   "lake naivasha beach", "Public Beach, Karagita, Naivasha", "beach, public beach, karagita",
   """<h2>Lake Naivasha Beach - Public Beach Karagita</h2>
<p><strong>Lake Naivasha Beach</strong> at Karagita is where all the action happens. This is the main launch point for boat rides and the heart of lakeside tourism.</p>
<h3>Getting Here</h3><p>From Naivasha town, take Moi South Lake Road for 5 km. Turn at the Karagita junction and follow signs to Public Beach.</p>
<h3>What You'll Find</h3><ul><li>Boat operators (look for Rafiki!)</li><li>Fresh grilled tilapia restaurants</li><li>Souvenir shops</li><li>Hippo watching from shore</li><li>Mt. Longonot views</li></ul>
<h3>Book a Boat Ride</h3><p>WhatsApp +254 701 215 295. Daily 6:30 AM - 6:30 PM.</p>""")

LP("Sunset Cruises Naivasha",
   "sunset-cruises-naivasha",
   "Sunset Cruises Naivasha | Golden Hour Boat Rides - Rafiki",
   "Book a magical sunset cruise on Lake Naivasha. Golden hour boat rides perfect for couples, proposals, birthdays. Private and group options.",
   "sunset cruises naivasha", "Lake Naivasha", "sunset, cruise, romantic, golden hour",
   """<h2>Sunset Cruises on Lake Naivasha</h2>
<p>A <strong>sunset cruise in Naivasha</strong> is the most romantic experience on the lake. Watch the golden sun dip behind the Rift Valley hills from the water.</p>
<h3>The Experience</h3><p>Depart at 4:00 PM and cruise the western channels where the sunset light is most spectacular. Your guide navigates to the perfect viewpoint as colors change from gold to amber to deep crimson.</p>
<h3>Perfect For</h3><ul><li>Couples and date nights</li><li>Proposals (we help coordinate!)</li><li>Anniversaries and honeymoons</li><li>Birthdays and celebrations</li><li>Photography enthusiasts</li></ul>
<h3>Add-ons</h3><p>Champagne, decorations, and photography available on request.</p>
<p>Book your sunset cruise: WhatsApp +254 701 215 295.</p>""")

LP("Crescent Island Tours",
   "crescent-island-tours",
   "Crescent Island Tours | Walking Safari Lake Naivasha - Rafiki",
   "Book Crescent Island tours from Lake Naivasha. Boat transfer + walking safari among giraffes and zebras. No fences, no vehicles.",
   "crescent island tours", "Crescent Island, Lake Naivasha", "crescent island, walking safari, giraffes",
   """<h2>Crescent Island Tours from Lake Naivasha</h2>
<p><strong>Crescent Island</strong> is Kenya's most unique walking safari destination. Walk freely among giraffes, zebras, and wildebeest - no fences, no vehicles.</p>
<h3>The Tour</h3><ol><li>Scenic boat ride from Public Beach (15 min)</li><li>Walking safari on the island (1-2 hours)</li><li>Return boat ride with different route</li></ol>
<h3>Wildlife You'll See</h3><ul><li>Giraffes - walk right next to them</li><li>Zebras - herds grazing freely</li><li>Wildebeest, waterbuck, elands</li><li>100+ bird species</li></ul>
<h3>Fun Facts</h3><p>Crescent Island was a filming location for "Out of Africa." The name comes from its crescent shape when water levels are high.</p>
<p>Book your tour: WhatsApp +254 701 215 295.</p>""")

LP("Bird Watching Lake Naivasha",
   "bird-watching-lake-naivasha",
   "Bird Watching Lake Naivasha | 400+ Species - Rafiki Boat Tours",
   "Lake Naivasha is a designated Important Bird Area with 400+ species. Join a bird watching boat tour. Fish Eagles, pelicans, kingfishers.",
   "bird watching lake naivasha", "Lake Naivasha", "birds, birding, ornithology, fish eagle",
   """<h2>Bird Watching on Lake Naivasha</h2>
<p>Lake Naivasha is a designated <strong>Important Bird Area (IBA)</strong> with 400+ recorded species. A boat ride here is a floating bird hide.</p>
<h3>Top Species</h3><ul><li>African Fish Eagle - iconic hunting dives</li><li>Great White Pelicans - group fishing</li><li>Malachite Kingfisher - jewel-colored</li><li>African Jacana - walks on lily pads</li><li>Goliath Heron - Africa's largest heron</li><li>Grey Crowned Crane - Kenya's symbol</li></ul>
<h3>Best Birding Times</h3><p>Early morning (6:30-9 AM). November-March for migratory species. Rainy seasons for peak diversity.</p>
<p>Book a birding tour: WhatsApp +254 701 215 295.</p>""")

LP("Boat Safari Lake Naivasha",
   "boat-safari-lake-naivasha",
   "Boat Safari Lake Naivasha | Wildlife Tours by Boat - Rafiki",
   "Experience the best boat safari on Lake Naivasha. See hippos, 400+ birds, and stunning landscapes on a guided wildlife boat tour.",
   "boat safari lake naivasha", "Lake Naivasha", "safari, wildlife, hippo, nature",
   """<h2>Boat Safari on Lake Naivasha</h2>
<p>A <strong>boat safari</strong> on Lake Naivasha combines the thrill of a wildlife safari with the serenity of being on water.</p>
<h3>Safari Routes</h3><ul><li>Hippo Channel Route - main hippo pods</li><li>Crescent Island Circuit - giraffes and zebras from water</li><li>Fisherman's Route - pelican colonies</li><li>Sunset Route - golden hour views</li></ul>
<h3>What Sets Us Apart</h3><p>deep local lake knowledge, local guides who know every channel, small groups (max 8), flexible routes based on wildlife activity.</p>
<p>Book your safari: WhatsApp +254 701 215 295.</p>""")

LP("Hippo Point Naivasha",
   "hippo-point-naivasha",
   "Hippo Point Naivasha | Best Hippo Sightings - Rafiki Boat Rides",
   "Visit Hippo Point on Lake Naivasha for the best hippo sightings. Guided boat tours to hippo pods. Photography opportunities.",
   "hippo point naivasha", "Hippo Point, Lake Naivasha", "hippo, wildlife, photography",
   """<h2>Hippo Point Naivasha</h2>
<p><strong>Hippo Point</strong> is one of Lake Naivasha's most iconic locations, named for the large pods that gather in this area.</p>
<h3>Why Visit</h3><p>Hippo sightings here are virtually guaranteed. Shallow waters and lush papyrus create perfect habitat. Morning visits offer the most activity.</p>
<h3>Getting There</h3><p>Accessible by boat from Public Beach with Rafiki. Our guides know the best viewing spots and approach angles.</p>
<p>Visit Hippo Point: WhatsApp +254 701 215 295.</p>""")

LP("Elsamere Conservation Centre",
   "elsamere-conservation-centre",
   "Elsamere Conservation Centre | Joy Adamson's Home - Lake Naivasha",
   "Visit Elsamere Conservation Centre on Lake Naivasha. Home of Joy Adamson, afternoon tea, colobus monkeys, and beautiful lakeside gardens.",
   "elsamere conservation centre", "Elsamere, Lake Naivasha", "elsamere, joy adamson, born free, conservation",
   """<h2>Elsamere Conservation Centre</h2>
<p><strong>Elsamere</strong> was the home of Joy Adamson, author of "Born Free." Now a conservation centre on Lake Naivasha's shores.</p>
<h3>What to Do</h3><ul><li>Afternoon tea on the lawn (3 PM daily)</li><li>Watch colobus monkeys swing through trees</li><li>Tour the museum about Joy's life</li><li>Enjoy the lakeside gardens</li></ul>
<h3>Combine with a Boat Ride</h3><p>We can arrange boat drop-off at Elsamere's jetty during your Lake Naivasha trip.</p>
<p>Plan your visit: WhatsApp +254 701 215 295.</p>""")

LP("Lake Naivasha Safari and Boat Ride",
   "lake-naivasha-safari-boat-ride",
   "Lake Naivasha Safari and Boat Ride | Wildlife & Water Adventure",
   "Combine a Lake Naivasha safari with a boat ride. See hippos from the water and giraffes on land. The complete wildlife experience.",
   "lake naivasha safari and boat ride", "Lake Naivasha", "safari, boat ride, wildlife, combo",
   """<h2>Lake Naivasha Safari and Boat Ride</h2>
<p>The ultimate Naivasha experience combines a <strong>safari and boat ride</strong> - see hippos from the water and walk among giraffes on land.</p>
<h3>The Combo Experience</h3><ol><li>Morning boat safari - hippos, birds, scenic channels</li><li>Crescent Island walking safari - giraffes, zebras up close</li><li>Optional: Sunset cruise to cap the day</li></ol>
<h3>Why Combine?</h3><p>You get both water and land wildlife in one trip. Our packages are designed to maximize your time and minimize waiting.</p>
<p>Book the combo: WhatsApp +254 701 215 295.</p>""")

LP("Naivasha Tour Packages",
   "naivasha-tour-packages",
   "Naivasha Tour Packages | Day Trips & Multi-Day Tours - Rafiki",
   "Complete Naivasha tour packages - half-day, full-day, weekend. Boat rides, Crescent Island, Hell's Gate. From Nairobi day trips.",
   "naivasha tour packages", "Naivasha", "tour packages, day trip, nairobi, weekend",
   """<h2>Naivasha Tour Packages</h2>
<p>We offer complete <strong>Naivasha tour packages</strong> for every schedule and budget.</p>
<h3>Half-Day (3-4 hours)</h3><p>Boat ride + Crescent Island. Perfect for day-trippers from Nairobi.</p>
<h3>Full-Day (6-7 hours)</h3><p>Morning safari + Crescent Island + lunch + sunset cruise.</p>
<h3>Weekend Package</h3><p>Day 1: Boat safari + sunset cruise. Day 2: Hell's Gate + Elsamere. Accommodation recommendations included.</p>
<h3>Custom Packages</h3><p>We create packages for groups, families, couples, schools, and corporate teams.</p>
<p>Design your package: WhatsApp +254 701 215 295.</p>""")

LP("Tour Lake Naivasha",
   "tour-lake-naivasha",
   "Tour Lake Naivasha | Guided Boat Tours & Safaris - Rafiki",
   "Tour Lake Naivasha with Rafiki Boat Rides. Guided boat tours, walking safaris, sunset cruises. deep local experience. Book today.",
   "tour lake naivasha", "Lake Naivasha", "tour, guided, boat, lake naivasha",
   """<h2>Tour Lake Naivasha with Rafiki</h2>
<p>Ready to <strong>tour Lake Naivasha</strong>? We offer the most comprehensive and trusted touring experience on the lake.</p>
<h3>Tour Options</h3><ul><li>Guided boat tour (1-3 hours)</li><li>Crescent Island walking tour</li><li>Sunset photography tour</li><li>Bird watching specialist tour</li><li>Full-day exploration tour</li></ul>
<h3>Our Guides</h3><p>Local experts who grew up on these waters. deep local guiding experience. Fluent in English and Swahili.</p>
<p>Start your tour: WhatsApp +254 701 215 295.</p>""")

LP("Boat Ride at Lake Naivasha",
   "boat-ride-at-lake-naivasha",
   "Boat Ride at Lake Naivasha | Hippo Safari & Wildlife Tours",
   "Take a boat ride at Lake Naivasha with Rafiki. See hippos, birds, and stunning scenery. From KES 1,000. Book your ride today.",
   "boat ride at lake naivasha", "Lake Naivasha", "boat ride, at, lake naivasha, hippo",
   """<h2>Boat Ride at Lake Naivasha</h2>
<p>A <strong>boat ride at Lake Naivasha</strong> is the definitive Kenya lake experience. Hippos, Fish Eagles, and breathtaking scenery await.</p>
<h3>What You'll Experience</h3><p>Board at Public Beach, Karagita, and glide through papyrus channels into the open lake. Encounter hippo pods, watch Fish Eagles hunt, and cruise past Crescent Island.</p>
<h3>Options</h3><ul><li>Standard ride: 1 hour from KES 1,000</li><li>Extended safari: 2 hours</li><li>Crescent Island combo: 2-3 hours</li><li>Sunset cruise: 1.5-2 hours</li></ul>
<p>Book now: WhatsApp +254 701 215 295. Daily 6:30 AM - 6:30 PM.</p>""")

LP("Boat Ride in Lake Naivasha",
   "boat-ride-in-lake-naivasha",
   "Boat Ride in Lake Naivasha | Guided Wildlife Tours - Rafiki",
   "Enjoy a guided boat ride in Lake Naivasha. Hippo watching, bird safari, Crescent Island transfers. Built around friendly local service.",
   "boat ride in lake naivasha", "Lake Naivasha", "boat ride, in, lake naivasha",
   """<h2>Boat Ride in Lake Naivasha</h2>
<p>There's nothing quite like a <strong>boat ride in Lake Naivasha</strong>. The freshwater lake is home to hippos, 400+ bird species, and some of the most beautiful scenery in Kenya's Rift Valley.</p>
<h3>Your Guide</h3><p>Rafiki Boat Rides has been providing boat rides in Lake Naivasha for many seasons. Our guides are local experts born and raised on these shores.</p>
<h3>Experiences</h3><ul><li>Hippo safari - see pods up close</li><li>Bird watching - Fish Eagles, pelicans, kingfishers</li><li>Crescent Island - walk among giraffes</li><li>Sunset cruise - golden hour magic</li></ul>
<p>Book: WhatsApp +254 701 215 295. Open daily 6:30 AM - 6:30 PM.</p>""")

LP("Boat Ride on Lake Naivasha",
   "boat-ride-on-lake-naivasha",
   "Boat Ride on Lake Naivasha | Wildlife Safari by Water - Rafiki",
   "Take a boat ride on Lake Naivasha with Rafiki. See hippos, birds, Crescent Island. friendly, deep local experience. Book today.",
   "boat ride on lake naivasha", "Lake Naivasha", "boat ride, on, lake naivasha",
   """<h2>Boat Ride on Lake Naivasha</h2>
<p>A <strong>boat ride on Lake Naivasha</strong> puts you at the heart of one of East Africa's most important freshwater ecosystems.</p>
<h3>The Experience</h3><p>From the moment you leave shore, you enter a world of hippos surfacing with dramatic snorts, Fish Eagles swooping overhead, and pelicans fishing in formation.</p>
<h3>Why Rafiki?</h3><p>guest-first reputation. verified guest feedback. deep local experience guiding on the lake. Woman-owned. Locally operated.</p>
<h3>Book Your Ride</h3><p>WhatsApp +254 701 215 295. Public Beach, Karagita. Daily 6:30 AM - 6:30 PM. Group discounts available.</p>""")

# Add new internal links
new_links = [
    ('boat rides in Naivasha', '/boat-rides-naivasha/'),
    ('sunset cruises', '/sunset-cruises-naivasha/'),
    ('Naivasha tour', '/naivasha-tour-packages/'),
    ('tour Lake Naivasha', '/tour-lake-naivasha/'),
    ('Elsamere', '/elsamere-conservation-centre/'),
    ('Hippo Point', '/hippo-point-naivasha/'),
    ('Lake Naivasha safari', '/lake-naivasha-safari-boat-ride/'),
    ('boat ride at Lake Naivasha', '/boat-ride-at-lake-naivasha/'),
    ('boat ride in Lake Naivasha', '/boat-ride-in-lake-naivasha/'),
    ('boat ride on Lake Naivasha', '/boat-ride-on-lake-naivasha/'),
]

print("\n--- Creating Internal Links ---")
for kw, url in new_links:
    link, created = InternalLink.objects.update_or_create(
        keyword=kw, defaults={'url': url, 'is_active': True})
    print(f"  [{'NEW' if created else 'UPD'}] '{kw}' -> {url}")

total_faqs = FAQ.objects.filter(is_active=True).count()
total_pages = LocalPage.objects.filter(is_active=True).count()
total_links = InternalLink.objects.filter(is_active=True).count()
print(f"\nDone! FAQs: {total_faqs} | Local Pages: {total_pages} | Internal Links: {total_links}")
