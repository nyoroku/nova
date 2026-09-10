"""
Phase 11: Seed to 500 total FAQs.
Fixed version: no infinite loops. Uses indexed, guaranteed-unique question generation.
Run: .venv\\Scripts\\python.exe seed_phase11_500_faqs.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import FAQ

print("=" * 60)
print("PHASE 11: FAQ SEEDER (TARGET: 500 TOTAL)")
print("=" * 60)

current_count = FAQ.objects.filter(is_active=True).count()
print(f"Current active FAQs: {current_count}")
needed = 500 - current_count
print(f"FAQs needed to reach 500: {needed}")

if needed <= 0:
    print("Already have 500+ FAQs. Exiting.")
    sys.exit(0)

# ====================================================================
# BUILD A FIXED, GUARANTEED-UNIQUE FAQ LIST
# Uses indexed combinations so no duplicate-check loops needed.
# ====================================================================

hotels = [
    "Enashipai Resort and Spa", "Lake Naivasha Sopa Resort", "Lake Naivasha Simba Lodge",
    "Kiboko Luxury Camp", "Sawela Lodges", "Lake Naivasha Country Club",
    "Chui Lodge", "Great Rift Valley Lodge", "Naivasha Kongoni Lodge", "Crescent Camp",
    "Fish Eagle Inn", "Lake Naivasha Dream Place", "Oloidien Bay Camp", "Naivasha Eco Camp"
]

locations = [
    "Nairobi", "Ruiru", "Mombasa", "Kisumu", "Kiambu", "Thika",
    "Limuru", "Gilgil", "Mai Mahiu", "Nakuru", "Eldoret",
    "Nyeri", "Nanyuki", "Kericho", "Machakos", "Embu",
    "Narok", "Bungoma", "Muranga", "Laikipia"
]

hours_map = {
    "Nairobi": "1.5", "Kiambu": "1.5", "Limuru": "1.5",
    "Ruiru": "2", "Thika": "2", "Gilgil": "1", "Mai Mahiu": "1",
    "Nakuru": "1.5", "Kisumu": "4", "Mombasa": "7",
    "Eldoret": "3.5", "Nyeri": "2.5", "Nanyuki": "3",
    "Kericho": "3", "Machakos": "2", "Embu": "3",
    "Narok": "2.5", "Bungoma": "5", "Muranga": "2", "Laikipia": "3.5"
}

landmarks = [
    "Hell's Gate National Park", "Mount Longonot", "Crater Lake Sanctuary",
    "Olkaria Geothermal Spa", "Crescent Island Game Sanctuary", "Sanctuary Farm",
    "Elsamere Conservation Centre", "Hippo Point", "Malewa River Delta",
    "South Lake Road", "Kongoni Game Valley", "Oserian Wildlife Sanctuary"
]

seasons = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ====================================================================
# FIXED HAND-CRAFTED FAQs (competitor, high-intent, general)
# ====================================================================
fixed_faqs = [
    # Competitor
    ("How does Gitoh B Boat Rides Naivasha compare to Rafiki?",
     "<p>While <strong>Gitoh B Boat Rides Naivasha</strong> is a popular operator, Rafiki provides premium private charters with certified infant life jackets and professional naturalist guides explaining the lake's papyrus ecology.</p>",
     "Rafiki offers certified infant safety gear, naturalist guides, and private charters that Gitoh B does not.", "booking", 601),

    ("Are Gitoh B Boat Rides Naivasha reviews positive?",
     "<p>Yes, Gitoh B reviews are generally friendly. However, Rafiki holds a consistent <strong>guest-first reputation</strong> for superior safety, cleaner hulls, and broker-free direct booking.</p>",
     "Gitoh B reviews are friendly, but Rafiki holds a guest-first reputation for safety and direct booking.", "booking", 602),

    ("How do Marina Boat Safaris Naivasha rates compare to Rafiki?",
     "<p><strong>Marina Boat Safaris Naivasha</strong> offers standard group tours. Rafiki offers flat-rate private charters that are cost-effective for groups of 3 or more traveling together.</p>",
     "Marina offers shared group tours; Rafiki offers flat-rate private charters cheaper for groups.", "pricing", 603),

    ("Does Gitoh B Naivasha offer sunset cruises?",
     "<p>Yes, Gitoh B runs sunset trips. Rafiki specializes in customized <strong>romantic sunset cruises</strong> with wine arrangements and photography-optimized positioning along the Mau escarpment channels.</p>",
     "Rafiki specializes in romantic sunset cruises with wine and optimal photography angles.", "booking", 604),

    ("Which is better — Marina Boat Safaris or Rafiki for hippo watching?",
     "<p>For dedicated hippo safaris, Rafiki is recommended. Our captains know exact hippo pod locations year-round and apply slow-drift photography approach techniques not available with standard operators.</p>",
     "Rafiki is recommended for hippo safaris due to expert captain knowledge and slow-drift approach techniques.", "booking", 605),

    # High-intent pricing
    ("How much is a Lake Naivasha boat ride?",
     "<p><strong>A shared Lake Naivasha boat ride costs KES 1,000–2,000 per person</strong> for group tours. A fully private charter is KES 4,000–8,000 per boat per hour for exclusive group use. Message WhatsApp +254 701 215 295.</p>",
     "Shared rides cost KES 1,000-2,000 per person; private charters cost KES 4,000-8,000 per boat per hour.", "pricing", 901),

    ("What is the best time of day for a Lake Naivasha boat ride?",
     "<p><strong>Early morning (7:00 AM – 9:00 AM)</strong> is the best time — water is mirror-calm, winds are minimal, and hippos and fish eagles are most active on the lake surface.</p>",
     "Early morning (7:00-9:00 AM) is optimal: calm water, no wind, and peak hippo and fish eagle activity.", "timing", 902),

    ("Does Lake Naivasha have an entrance fee?",
     "<p><strong>No. Lake Naivasha does not have a mandatory entrance fee.</strong> You only pay for your boat charter. Crescent Island Sanctuary has a separate conservation entry fee paid on arrival.</p>",
     "No. Lake Naivasha has no entrance fee. You only pay for your boat charter.", "pricing", 903),

    ("How much is the maid of the mist boat ride?",
     "<p>The Maid of the Mist is at Niagara Falls, USA. For an equivalent dramatic freshwater safari in East Africa, book a <strong>Rafiki Hippo Boat Safari on Lake Naivasha</strong> — a wild hippo encounter surpassing any boat show ride.</p>",
     "The Maid of the Mist is at Niagara Falls. For East Africa, book a Rafiki hippo safari on Lake Naivasha.", "general", 904),

    ("What is the Lake Naivasha boat ride price per person?",
     "<p>Prices start at <strong>KES 1,000 per person per hour</strong> for shared rides from Karagita Beach. Private charters cost KES 4,000–6,000 flat-rate per boat — more economical for families of 3+.</p>",
     "Shared rides start at KES 1,000 per person. Private charters are KES 4,000-6,000 flat-rate per boat.", "pricing", 905),

    ("What is the Lake Naivasha boat ride price in Kenya shillings?",
     "<p>In Kenya shillings: <strong>shared group tours cost KES 1,000–2,000 per person</strong>, while exclusive private charters range from KES 4,000–8,000 per hour depending on boat type.</p>",
     "KES 1,000-2,000 per person for shared tours; KES 4,000-8,000 per hour for private charters.", "pricing", 906),

    ("What is the Lake Naivasha boat ride price from Nairobi as a day trip?",
     "<p>A full-day package from Nairobi including return transport, 2-hour boat safari, Crescent Island walk, and tilapia lunch ranges from <strong>KES 8,000–15,000 per person</strong> depending on group size.</p>",
     "A full Nairobi day package with transport, boat safari, and lunch costs KES 8,000-15,000 per person.", "pricing", 907),

    ("Where can I find pontoon boat rides in Naivasha?",
     "<p>Rafiki offers <strong>luxury pontoon boat rides on Lake Naivasha</strong> with flat decks, leather seating, and shade canopies — ideal for corporate events, birthdays, and large family outings.</p>",
     "Rafiki offers luxury pontoon charters with flat decks and shade canopies for groups and events.", "booking", 908),

    ("Is a pontoon boat safer than a speedboat on Lake Naivasha?",
     "<p>Both are very safe with Rafiki. Pontoon boats offer maximum stability and deck space for large groups, while fiberglass speedboats allow agile navigation through papyrus channels for wildlife photography.</p>",
     "Both are safe. Pontoons give maximum stability; speedboats allow agile papyrus channel navigation.", "safety", 909),

    ("Are there boat rides in Ruiru, Kenya?",
     "<p>Ruiru has small dam recreational boats (like Titanic Dam). For a true natural lake wildlife experience, take the 1.5-hour drive to <strong>Lake Naivasha for a Rafiki hippo safari</strong> — incomparably richer.</p>",
     "Ruiru has small dam boats. Lake Naivasha, 1.5 hours away, offers a true hippo and wildlife safari.", "destination", 910),

    ("Where can I go boat riding in Nairobi?",
     "<p>Nairobi has limited boat riding at Uhuru Park and Paradise Lost in Kiambu. For authentic wildlife safaris, travel to <strong>Lake Naivasha</strong> — just 1.5 hours from the city centre.</p>",
     "Uhuru Park and Paradise Lost offer small boats. Lake Naivasha, 1.5 hours away, is the true wildlife destination.", "destination", 911),

    ("How do I book a Crescent Island boat ride transfer?",
     "<p>Book with Rafiki via WhatsApp (+254 701 215 295). We provide a direct flat-rate return boat transfer from Karagita Beach, wait at the dock during your walking safari, and bring you back safely.</p>",
     "Book via WhatsApp. We provide return transfer and wait at the dock during your Crescent Island walk.", "booking", 912),

    ("Can I do a corporate team building event on a pontoon boat on Lake Naivasha?",
     "<p><strong>Yes, absolutely.</strong> Our luxury pontoon boats accommodate up to 30 passengers in a circular seating layout, perfect for facilitated wildlife-themed team building activities.</p>",
     "Yes, our pontoon boats seat up to 30 passengers and are ideal for wildlife-themed corporate team building.", "booking", 913),

    ("What are the environmental regulations for boats on Lake Naivasha?",
     "<p>All operators must use <strong>four-stroke low-emission outboard engines</strong>, maintain a 50-meter hippo buffer, enforce 100% plastic-free policies, and carry licensed Kenya Maritime Authority certification.</p>",
     "Operators must use low-emission engines, maintain hippo buffers, and carry KMA certification.", "safety", 914),

    ("Why is papyrus grass critical to Lake Naivasha's health?",
     "<p>Papyrus acts as a <strong>biological filtration system</strong>, trapping silt from the Malewa River, absorbing agricultural chemical runoff, and providing essential nesting habitat for 400+ bird species and juvenile fish shelter.</p>",
     "Papyrus filters silt and chemicals, and provides nesting habitat for 400+ bird species.", "general", 915),

    ("Can we see Mount Longonot from the boat?",
     "<p><strong>Yes.</strong> On clear mornings, Mount Longonot's massive volcanic crater dominates the southern horizon from the boat, creating spectacular landscape photography backdrops.</p>",
     "Yes, Mount Longonot's volcanic crater is clearly visible on the southern horizon from the lake.", "location", 916),

    ("Why are there dead trees standing in Lake Naivasha?",
     "<p>Rising lake levels over recent decades submerged what were once lakeside acacia forests. These dead standing trees now serve as elevated perch sites for <strong>African Fish Eagles</strong> and nesting cormorants.</p>",
     "Rising water levels submerged lakeside acacias, which now serve as perch sites for fish eagles.", "general", 917),

    ("What is the best month to see Lesser Flamingos at Lake Naivasha?",
     "<p>January to March is best — receding water levels in Oloidien Bay increase alkalinity, attracting massive <strong>Lesser Flamingo flocks</strong> to feed on blue-green algae along the shallows.</p>",
     "January to March is best. Receding water in Oloidien Bay increases alkalinity attracting flamingo flocks.", "timing", 918),

    ("Do you offer school group discounts for environmental field trips?",
     "<p>Yes. Rafiki offers <strong>educational pricing for school groups</strong> covering papyrus biology, hippo behavior, fish eagle ecology, and sustainable fisheries — aligned with Kenya's CBC curriculum science objectives.</p>",
     "Yes, we offer school group discounts covering papyrus biology, hippo behavior, and bird ecology.", "pricing", 919),

    ("Are there private guides for the Crescent Island walking safari?",
     "<p>Yes. Professional island naturalist guides accompany you on foot at Crescent Island, ensuring safe distances from giraffes, elands, and wildebeests while explaining their ecology and behavior.</p>",
     "Yes, island naturalist guides accompany your walk, ensuring safe approach to giraffes and zebras.", "booking", 920),
]

# ====================================================================
# PROGRAMMATICALLY GENERATED FAQs — INDEXED, NO INFINITE LOOPS
# ====================================================================

# Hotel questions (5 templates × 14 hotels = 70 unique FAQs)
hotel_question_templates = [
    ("Can I get a direct boat pickup from {h}?",
     "<p><strong>Yes.</strong> Rafiki arranges direct boat pickup from the private jetty at <strong>{h}</strong>, saving you the drive to Karagita Beach and ensuring a seamless boarding experience.</p>",
     "Yes, we arrange direct pickup from the jetty at {h}.", "logistics"),
    ("How far is Karagita Beach from {h}?",
     "<p>Karagita Beach is approximately <strong>5–15 minutes by road</strong> from <strong>{h}</strong> along South Lake Road. We can also arrange direct jetty pickup from the hotel itself.</p>",
     "Karagita Beach is 5-15 minutes from {h} by road, or we can pick you up from their jetty.", "location"),
    ("Are hippos dangerous near the shoreline of {h}?",
     "<p>Hippos frequently graze on lakeside hotel lawns at night. <strong>Do not approach hippos on foot</strong> after dark. A daytime Rafiki boat safari is the only safe way to observe them up close.</p>",
     "Yes, hippos graze on hotel lawns at night. A daytime boat safari is the safest way to observe them.", "safety"),
    ("Can we book a sunset boat cruise that ends at {h}?",
     "<p>Yes. Rafiki can coordinate sunset cruises that <strong>return you directly to {h}'s private jetty</strong> just before dusk at 6:30 PM for a seamless end to your romantic evening.</p>",
     "Yes, we can return you to {h}'s jetty just before dusk at 6:30 PM.", "timing"),
    ("Does {h} have its own boat tours or should I book Rafiki?",
     "<p>Most hotels arrange boats through third-party operators at commission. Booking directly with <strong>Rafiki via WhatsApp (+254 701 215 295)</strong> guarantees the lowest rates and professionally certified safety standards.</p>",
     "Book directly with Rafiki for the lowest rates and certified safety, avoiding hotel commission markups.", "booking"),
]

# Location questions (5 templates × 20 locations = 100 unique FAQs)
location_question_templates = [
    ("How long is the drive from {l} to Lake Naivasha?",
     "<p>The drive from <strong>{l}</strong> to Lake Naivasha takes approximately <strong>{h} hours</strong> via the B3 highway past the Rift Valley Escarpment viewpoint. Depart early to avoid traffic.</p>",
     "The drive from {l} to Lake Naivasha takes about {h} hours. Depart early to avoid traffic.", "logistics"),
    ("Is a boat ride in Naivasha better than boat riding near {l}?",
     "<p><strong>Yes.</strong> Lake Naivasha is a 139 km² natural Rift Valley lake with 1,500+ hippos and 400+ bird species — incomparable to any artificial recreational dam or pond available near <strong>{l}</strong>.</p>",
     "Lake Naivasha vastly surpasses any artificial dam near {l} with 1,500 hippos and 400 bird species.", "destination"),
    ("Can I do a day trip from {l} for a Lake Naivasha boat safari?",
     "<p>Yes! Departing early from <strong>{l}</strong>, a day trip easily covers: a 2-hour hippo boat safari, Crescent Island walking tour, fresh tilapia lunch at Karagita Beach, and return home by evening.</p>",
     "Yes, a day trip from {l} can include a boat safari, Crescent Island walk, tilapia lunch, and return by evening.", "logistics"),
    ("What transport options are available from {l} to Naivasha?",
     "<p>From <strong>{l}</strong>, options include public matatus (affordable, KES 500–1,500), private taxis, and luxury hotel shuttle transfers. Rafiki can connect you with reliable private transfer services.</p>",
     "From {l}: public matatus (KES 500-1,500), private taxis, and hotel shuttles are all available.", "logistics"),
    ("What should I pack for a day trip from {l} to Lake Naivasha?",
     "<p>From <strong>{l}</strong>, pack: sunscreen and a wide-brim hat, a light windbreaker jacket (the lake breeze is cool), binoculars for birdwatching, a zoom camera lens, and comfortable walking shoes for Crescent Island.</p>",
     "Pack sunscreen, a windbreaker, binoculars, a camera with zoom lens, and walking shoes for Crescent Island.", "preparation"),
]

# Landmark questions (5 templates × 12 landmarks = 60 unique FAQs)
landmark_question_templates = [
    ("Can we combine {lm} with a Lake Naivasha boat ride?",
     "<p><strong>Yes — this is our most popular combination.</strong> Visit <strong>{lm}</strong> in the morning for activities, then relax on a private Rafiki afternoon hippo boat safari.</p>",
     "Visit {lm} in the morning, then enjoy an afternoon Rafiki hippo boat safari. Our most popular combo.", "booking"),
    ("How far is Karagita Beach from {lm}?",
     "<p>Rafiki's Karagita Beach launch point is approximately <strong>10–20 minutes by road</strong> from <strong>{lm}</strong>, making a combined day itinerary perfectly achievable.</p>",
     "Karagita Beach is 10-20 minutes from {lm}, making a combined day itinerary very manageable.", "location"),
    ("Do I need separate tickets for {lm} and the Rafiki boat safari?",
     "<p>Yes. <strong>{lm}</strong> entry fees are paid to the relevant park authority (KWS or private management). Boat safari fees are paid separately to Rafiki. Combined package pricing is available on request.</p>",
     "Yes, park fees for {lm} are paid separately. Ask Rafiki about combined package pricing.", "pricing"),
    ("Is {lm} suitable for children and families?",
     "<p>Yes, <strong>{lm}</strong> is highly family-friendly and pairs beautifully with a safe, child-optimized Rafiki boat ride featuring infant life jackets and gentle wildlife commentary for young explorers.</p>",
     "{lm} is family-friendly and pairs well with Rafiki's child-safe boat safari with infant life jackets.", "safety"),
    ("What is the best time of day to visit {lm} before an afternoon boat ride?",
     "<p>For <strong>{lm}</strong>, morning hours (7:00–11:00 AM) offer the best light, temperatures, and animal activity. This leaves the perfect afternoon window for a 3:00–5:00 PM Rafiki hippo safari.</p>",
     "Visit {lm} in the morning (7-11 AM), then book a 3-5 PM Rafiki boat safari for peak hippo activity.", "timing"),
]

# Seasonal safety questions (1 template × 12 months = 12 unique FAQs)
seasonal_templates = [
    ("Is Lake Naivasha safe for boat rides in {s}?",
     "<p>Yes. Lake Naivasha is safe year-round. In <strong>{s}</strong>, Rafiki captains conduct daily weather checks and may adjust departure times to avoid afternoon wind build-up that occasionally affects the open lake channels.</p>",
     "Yes, Lake Naivasha is safe in {s}. Captains adjust timing to avoid afternoon wind on the open lake.", "safety"),
]

# ====================================================================
# BUILD THE FAQ LIST DETERMINISTICALLY
# ====================================================================
faq_data = list(fixed_faqs)
order_counter = 1000

# Add hotel FAQs
for h_idx, hotel in enumerate(hotels):
    for t_idx, template in enumerate(hotel_question_templates):
        q = template[0].format(h=hotel)
        a = template[1].format(h=hotel)
        plain = template[2].format(h=hotel)
        intent = template[3]
        order_counter += 1
        faq_data.append((q, a, plain, intent, order_counter))

# Add location FAQs
for l_idx, loc in enumerate(locations):
    hrs = hours_map.get(loc, "3")
    for t_idx, template in enumerate(location_question_templates):
        q = template[0].format(l=loc)
        a = template[1].format(l=loc, h=hrs)
        plain = template[2].format(l=loc, h=hrs)
        intent = template[3]
        order_counter += 1
        faq_data.append((q, a, plain, intent, order_counter))

# Add landmark FAQs
for lm_idx, lm in enumerate(landmarks):
    for t_idx, template in enumerate(landmark_question_templates):
        q = template[0].format(lm=lm)
        a = template[1].format(lm=lm)
        plain = template[2].format(lm=lm)
        intent = template[3]
        order_counter += 1
        faq_data.append((q, a, plain, intent, order_counter))

# Add seasonal FAQs
for s in seasons:
    q = seasonal_templates[0][0].format(s=s)
    a = seasonal_templates[0][1].format(s=s)
    plain = seasonal_templates[0][2].format(s=s)
    intent = seasonal_templates[0][3]
    order_counter += 1
    faq_data.append((q, a, plain, intent, order_counter))

print(f"Total unique FAQs compiled: {len(faq_data)}")
print(f"FAQs needed: {needed}")

# Trim to only what's needed
faq_data = faq_data[:needed]
print(f"FAQs to insert: {len(faq_data)}")

# ====================================================================
# BULK INSERT — NO INFINITE LOOPS
# ====================================================================
created_count = 0
updated_count = 0

for i, (q, a, plain, intent, order) in enumerate(faq_data, 1):
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
    if created:
        created_count += 1
    else:
        updated_count += 1
    if i % 50 == 0:
        print(f"  Progress: {i}/{len(faq_data)} FAQs inserted...")

print(f"\n{'=' * 60}")
print(f"PHASE 11 COMPLETE!")
print(f"  FAQs Created: {created_count}")
print(f"  FAQs Updated: {updated_count}")
print(f"  Total Active FAQs: {FAQ.objects.filter(is_active=True).count()}")
print(f"{'=' * 60}")
