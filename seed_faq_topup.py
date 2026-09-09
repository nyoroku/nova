"""
FAQ Top-up: Adds exactly 8 brand-new unique FAQs to reach 500 total.
Run: .venv\Scripts\python.exe seed_faq_topup.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from seo.models import FAQ

print("=" * 60)
print("FAQ TOP-UP: ADDING 8 UNIQUE FAQs TO REACH 500")
print("=" * 60)

current_count = FAQ.objects.filter(is_active=True).count()
print(f"Current active FAQs: {current_count}")
needed = 500 - current_count

if needed <= 0:
    print("Already have 500+ FAQs. Exiting.")
    sys.exit(0)

print(f"FAQs needed: {needed}")

# 8 guaranteed brand-new unique FAQs
topup_faqs = [
    (
        "What time does the last boat depart at Lake Naivasha with Rafiki?",
        "<p>The last boat departure at Lake Naivasha with <strong>Rafiki</strong> is typically at <strong>5:30 PM</strong>, giving guests time for a beautiful sunset on the water before the park closes. Early morning departures start as early as 6:00 AM for bird watchers.</p>",
        "The last Rafiki boat departs at 5:30 PM. Morning departures start at 6:00 AM for bird watching.",
        "booking", 1010
    ),
    (
        "Does Rafiki provide life jackets for every passenger on Lake Naivasha?",
        "<p>Yes — <strong>Rafiki</strong> provides <strong>certified life jackets for every passenger</strong>, including infants. Our safety equipment is inspected regularly by the Kenya Maritime Authority. No passenger boards without a properly fitted life jacket.</p>",
        "Yes, Rafiki provides certified life jackets for every passenger including infants.",
        "safety", 1011
    ),
    (
        "Can I pay for a Lake Naivasha boat ride via M-Pesa with Rafiki?",
        "<p>Yes, <strong>Rafiki</strong> accepts <strong>M-Pesa payments</strong> for all boat ride bookings. You can pay via Paybill or use our website's online booking portal which supports mobile money. Cash and card payments are also accepted at the dock.</p>",
        "Yes, Rafiki accepts M-Pesa, cash, and card payments for boat ride bookings.",
        "booking", 1012
    ),
    (
        "What wildlife will I see on a Rafiki boat safari at Lake Naivasha?",
        "<p>On a <strong>Rafiki boat safari</strong> at Lake Naivasha, you can expect to see <strong>hippos</strong> surfacing near the papyrus reeds, <strong>African fish eagles</strong> swooping for prey, <strong>pelicans</strong>, <strong>cormorants</strong>, <strong>kingfishers</strong>, and over 100 other bird species. Water buffalo and zebra are visible from the shore near Crescent Island.</p>",
        "Expect to see hippos, African fish eagles, pelicans, cormorants, kingfishers, and 100+ bird species.",
        "experience", 1013
    ),
    (
        "How early should I arrive before a boat ride at Lake Naivasha?",
        "<p>We recommend arriving at the <strong>Karagita Public Beach</strong> at least <strong>15–20 minutes before your scheduled departure</strong>. This allows time for life jacket fitting, safety briefing, and boarding. For morning bird-watching trips, arriving by 5:45 AM is ideal.</p>",
        "Arrive 15-20 minutes early for life jacket fitting and safety briefing before boarding.",
        "logistics", 1014
    ),
    (
        "Is the Lake Naivasha boat ride suitable for elderly visitors?",
        "<p>Yes, Lake Naivasha boat rides with <strong>Rafiki</strong> are very suitable for elderly visitors. Our pontoon boats have <strong>stable flat decks, comfortable seating, and shade canopies</strong>. The water is calm and there are no rough currents. Our crew assists with boarding and ensures comfort throughout the ride.</p>",
        "Yes, our stable pontoon boats with comfortable seating and shade are ideal for elderly visitors.",
        "experience", 1015
    ),
    (
        "What is the best season to visit Lake Naivasha for a boat ride?",
        "<p>Lake Naivasha is beautiful <strong>year-round</strong>, but the <strong>dry seasons (January–March and July–October)</strong> offer the most pleasant conditions with clear skies and comfortable temperatures. The wet season (April–June) brings lush greenery and excellent bird breeding activity. Rafiki operates boat rides in all seasons.</p>",
        "Year-round visits are great. Dry seasons (Jan-Mar, Jul-Oct) give clearest skies; wet season adds lush greenery.",
        "logistics", 1016
    ),
    (
        "Can Rafiki arrange a private boat charter for a corporate event at Lake Naivasha?",
        "<p>Absolutely. <strong>Rafiki</strong> specialises in <strong>private pontoon boat charters</strong> for corporate team-building events, product launches, and company retreats at Lake Naivasha. We can accommodate groups of up to 30 people per boat with customised itineraries, catering arrangements, and naturalist guides. Contact us for a custom quote.</p>",
        "Yes, Rafiki offers private pontoon charters for corporate events, accommodating up to 30 people.",
        "booking", 1017
    ),
]

created_count = 0
for q, a, plain, intent, order in topup_faqs[:needed]:
    if FAQ.objects.filter(question=q).exists():
        print(f"  SKIP (exists): {q[:60]}")
        continue
    FAQ.objects.create(
        question=q,
        answer=a,
        plain_answer=plain,
        search_intent=intent,
        order=order,
        is_active=True,
        allow_indexing=True
    )
    created_count += 1
    print(f"  CREATED: {q[:60]}")

final_count = FAQ.objects.filter(is_active=True).count()
print(f"\nFAQ Top-up complete!")
print(f"  FAQs Created: {created_count}")
print(f"  Total Active FAQs: {final_count}")
print("=" * 60)
