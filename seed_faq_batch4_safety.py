"""Batch 4: Safety, Health, Weather, and Packing FAQs"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import FAQ

def F(q, a, plain, intent, order):
    dupes = FAQ.objects.filter(question=q)
    if dupes.count() > 1:
        keep = dupes.order_by('-id').first()
        dupes.exclude(id=keep.id).delete()
    faq, created = FAQ.objects.update_or_create(question=q, defaults={
        'answer': a, 'plain_answer': plain, 'search_intent': intent,
        'order': order, 'is_active': True, 'allow_indexing': True})
    print(f"  [{'NEW' if created else 'UPD'}] {q}")

faqs = [
    ("Is there Bilharzia in Lake Naivasha?", "<p>While some older guidebooks suggest otherwise, <strong>there is no modern risk of Bilharzia at Lake Naivasha</strong>, due to the high altitude (1,884m) and cooler water temperatures.</p>", "No modern risk of Bilharzia at Lake Naivasha due to the high altitude and water temperatures.", "health", 401),
    ("Can I get Malaria at Lake Naivasha?", "<p>The high 1,884m altitude means Lake Naivasha is outside primary Anopheles mosquito breeding zones. <strong>Malaria risk is considered heavily negligible.</strong></p>", "Malaria risk is considered heavily negligible because the high altitude prevents mosquito breeding.", "health", 402),
    ("Are there Tsetse flies during the boat ride?", "<p><strong>Zero.</strong> Tsetse flies, which carry Sleeping Sickness, require arid scrub brush and do not exist anywhere near the Lake Naivasha ecosystem.</p>", "Zero. Tsetse flies require arid scrub bush and do not exist anywhere near Lake Naivasha.", "health", 403),
    ("What should I do if a hippo approaches our boat?", "<p>You should do nothing. Your Rafiki boat captain is trained to read the posturing and will gracefully reverse the boat to maintain a mandatory safety buffer.</p>", "Do nothing. Your trained captain will gracefully reverse the boat to maintain a mandatory safety buffer.", "safety", 404),
    ("Can children wear adult life jackets?", "<p><strong>No.</strong> Rafiki stocks specialized infant and properly fitted child-sized life jackets to guarantee the absolute safety of younger passengers.</p>", "No. Rafiki stocks specialized infant and well-fitted child-sized life jackets.", "safety", 405),
    ("Are the fiberglass hulls completely safe?", "<p><strong>Incredibly yes.</strong> We operate customized, wide commercial fiberglass hulls designed to easily withstand sudden hippo wakes without capsizing.</p>", "Incredibly yes. We operate customized commercial fiberglass hulls designed to easily withstand sudden hippo wakes.", "safety", 406),
    ("Do you inspect the tour boats daily?", "<p><strong>Yes.</strong> Every single outboard motor and fiberglass hull is professionally inspected prior to our first morning safari ride.</p>", "Yes. Every single outboard motor and fiberglass hull is professionally inspected prior to the first morning ride.", "safety", 407),
    ("What happens during a severe lightning storm?", "<p>We completely suspend all boat operations during electrical storms, prioritizing human safety over tourist schedules every single time.</p>", "We completely suspend all boat operations during electrical storms, prioritizing human safety over tourist schedules.", "safety", 408),
    ("Is the African midday sun dangerous?", "<p>At high equatorial altitudes, UV rays are quite aggressive. We highly recommend applying SPF 50 sunscreen prior to boarding the open boats.</p>", "Equatorial UV rays are quite aggressive. We recommend applying SPF 50 sunscreen prior to boarding.", "health", 409),
    ("Do the boats have shade coverings?", "<p>Some of our larger boats possess canvas tops, but smaller safari boats are completely open to maximize unobstructed sky photography.</p>", "Larger boats possess canvas tops, but smaller safari boats are completely open to maximize unobstructed sky photography.", "safety", 410),
    ("Can elderly passengers easily board?", "<p><strong>Yes.</strong> The fiberglass hulls sit perfectly stable parallel to the shallow Karagita sands, and our crew physically assists every single boarding.</p>", "Yes. The hulls sit perfectly stable parallel to the shallow Karagita sands. Our crew physically assists every boarding.", "safety", 411),
    ("What if a passenger faces a medical emergency?", "<p>Every Rafiki captain understands emergency response protocols, instantly accelerating the boat to the nearest private commercial medical jetty.</p>", "Every Rafiki captain understands emergency response protocols, instantly accelerating the boat to the nearest medical jetty.", "health", 412),
    ("Are waterproof raincoats normally provided?", "<p>During rainy seasons (April-May), heavy unpredictable downpours occur frequently. Clients must bring their own waterproof gear or ponchos.</p>", "During rainy seasons, clients must bring their own waterproof gear or ponchos to stay dry.", "preparation", 413),
    ("Can intense wind capsize the small boats?", "<p>While heavy 'lake blowouts' occur in late afternoons, <strong>our captains consistently cancel rides</strong> before conditions become unmanageable.</p>", "Our captains consistently cancel rides before conditions become unmanageable due to heavy lake blowouts.", "safety", 414),
    ("What is the best lens for photography from the boat?", "<p>For birding, we recommend a <strong>150-600mm telephoto lens</strong>. For stunning landscape shots of the escarpment, a 24-70mm lens is incredibly ideal.</p>", "For birding, we recommend a 150-600mm telephoto lens. For landscape shots, a 24-70mm lens is incredibly ideal.", "preparation", 415),
    ("Should I bring my binoculars on the boat?", "<p><strong>Absolutely.</strong> While the birdlife is incredibly close, a good pair of 8x42 binoculars massively enhances your ability to spot tiny birds in the papyrus.</p>", "Absolutely. A good pair of 8x42 binoculars massively enhances your ability to spot tiny birds in the papyrus.", "preparation", 416),
    ("Can I recharge my camera battery on the boat?", "<p><strong>No.</strong> Our small, open fiberglass safari boats do not have onboard electrical outlets. Ensure your camera batteries are fully charged beforehand.</p>", "No. Our small safari boats do not have onboard electrical outlets. Ensure your camera batteries are fully charged beforehand.", "preparation", 417),
    ("What should I wear for an early 6:00 AM ride?", "<p>Early mornings at 1,884m altitude are surprisingly cold. Layer up with a <strong>heavy fleece jacket and windbreaker</strong>, which you can shed later.</p>", "Early mornings at 1,884m altitude are cold. Layer up with a heavy fleece jacket and windbreaker, which you can shed later.", "preparation", 418),
    ("Do you provide a waterproof dry bag for cameras?", "<p>We strongly recommend bringing a reliable dry bag to shield your expensive electronics from random lake splashes and sudden rain.</p>", "We strongly recommend bringing a reliable dry bag to shield your electronics from random lake splashes and rain.", "preparation", 419),
    ("Is the tap water safe to blindly drink at my lodge?", "<p><strong>Generally no.</strong> While 5-star lodges filter their water, we strictly advise drinking entirely bottled water to avoid mild traveler's stomach illnesses.</p>", "Generally no. We strictly advise drinking entirely bottled water to avoid mild traveler's stomach illnesses.", "health", 420),
    ("Where is the closest functional hospital to Rafiki Boat Rides?", "<p>The heavily reliable <strong>Naivasha District Hospital</strong> and several highly modern private diagnostic clinics are located just 15 minutes away in Naivasha Town.</p>", "the reliable Naivasha District Hospital and several highly modern private clinics are located 15 minutes away.", "health", 421),
    ("What if I accidentally drop my phone in the lake?", "<p>Unfortunately, retrieving dropped electronics from the deeply muddy, fiercely dense papyrus bottom is essentially impossible. Hold your devices securely.</p>", "Unfortunately, retrieving dropped electronics from the deeply muddy, fiercely dense papyrus bottom is impossible. Hold devices securely.", "safety", 422),
    ("Can I casually smoke a cigarette on the boat?", "<p><strong>Strictly no.</strong> Due to the presence of flammable outboard fuel and closely seated passenger quarters, smoking is completely prohibited.</p>", "Strictly no. Due to the presence of flammable outboard fuel and closely seated passenger quarters, smoking is prohibited.", "safety", 423),
    ("Should I pack strong insect repellent?", "<p><strong>Yes.</strong> While safe from Malaria, you should pack a DEET-based repellent to ward off regular mosquitoes actively thriving near the evening shore.</p>", "Yes. Pack a DEET-based repellent to comfortably ward off regular mosquitoes actively thriving near the evening shore.", "preparation", 424),
    ("What kind of shoes are truly best for Crescent Island?", "<p>Avoid open sandals or heavy hiking boots. Light, closed-toe trail runners are naturally perfect for walking the grassy island trails.</p>", "Light, closed-toe trail runners are naturally perfect for walking the heavily grassy island trails.", "preparation", 425),
    ("Is walking alone completely safe in Karagita?", "<p>While safe during the day, tourists should stay near the busy beach launch and avoid walking alone in remote stretches at night.</p>", "While safe during the day, tourists should stay near the busy beach launch and avoid walking alone at night.", "safety", 426),
    ("Do you provide free drinking water for guests?", "<p>For luxury charters, yes. For public scheduled rides, passengers must bring their own bottled water to stay hydrated under the sun.</p>", "For luxury charters, yes. For scheduled rides, passengers must bring their own bottled water to stay hydrated under the sun.", "preparation", 427),
]

print("--- Starting Batch 4 FAQ Generation ---")
for q, a, plain, intent, order in faqs:
    F(q, a, plain, intent, order)
print("--- Batch 4 Complete (27 FAQs Injected) ---")
