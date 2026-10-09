from django.db import migrations

QUESTIONS = {
 'classic-lake-safari': [
    ('Can I choose shared seats or a private boat?', 'The current options distinguish shared seats from private boat bookings. Shared-seat prices apply per person; a private boat price covers the stated party limit. Nova confirms availability before booking.'),
    ('Does the one-hour ride include Crescent Island admission?', 'Sanctuary admission is not included in the standard boat service. If you want a water-and-land visit, explore the Crescent Island activity and check its separate admission fees.')],
 'hippo-bird-safari': [
    ('How does the hippo and bird safari differ from the introductory ride?', 'This experience focuses on observing wildlife and lake habitats. Choose an option for its current duration, and confirm the planned route with Nova. Extra time does not guarantee additional sightings.'),
    ('Will this safari guarantee hippo or fish eagle sightings?', 'No. The route offers opportunities to observe wildlife, but animals and birds move freely. Sightings vary with conditions and timing.')],
 'crescent-island': [
    ('How are boat charges and sanctuary admission separated?', 'The boat option covers the stated Nova service. Mandatory sanctuary admission depends on visitor category and eligibility and is itemized separately. Check the current fee schedule and full quote before booking.'),
    ('Does the walking safari include a sanctuary guide?', 'Confirm whether you want an independent visit or a walking guide. A separate guiding service is not assumed to be included in the boat charge; ask Nova to state the arrangement in your quote.')],
 'sunset-cruise': [
    ('Does the sunset cruise include food or drinks?', 'Meals, drinks and celebration extras are included only when expressly listed in your confirmed quote. The standard option describes the boat service.'),
    ('What if clouds obscure the sunset?', 'Sunset visibility cannot be guaranteed. Weather and safe lake conditions determine the departure and route; confirm the applicable weather and cancellation terms with Nova.')],
 'private-charter': [
    ('Will other guest parties join my private boat?', 'A private option reserves the boat for your party within the stated passenger limits. Tell Nova your party size and any route preferences before confirmation.'),
    ('How do hourly and longer charter options compare?', 'Each option has its own duration and rate. Compare the complete option rather than applying an hourly amount to an unrelated full-day charter. Additional hours and route changes require confirmation.')],
 'family-ride': [
    ('What information does Nova need for a family ride?', 'Include children’s ages, party size and any boarding or mobility needs. Nova needs this information to confirm appropriate life jackets and the suitable booking option.'),
    ('Do children automatically receive a discounted boat fare?', 'No discount is assumed. Private-boat prices cover the stated party limit; shared-seat child rates apply only when configured and confirmed. Ask for an itemized family quote.')],
 'photography-birding': [
    ('Does the photography tour provide camera equipment?', 'Bring your own camera equipment unless a confirmed quote expressly includes a separate equipment service. Discuss storage, positioning and the needs of your equipment with Nova.'),
    ('Can I request a specialist birding guide?', 'Discuss the birding support you need before booking. Nova should confirm the available captain or guide, their relevant experience and the selected session’s arrangements.')],
 'groups-events': [
    ('How does the group minimum booking work?', 'The current option states the minimum party size and the minimum transaction cost. Smaller parties should request another arrangement rather than assume the group rate applies.'),
    ('How are passengers allocated across boats?', 'Nova confirms boat allocation, individual passenger limits and departure coordination for your group. A group’s total party limit is not the capacity of one boat.')],
 'sunrise-wildlife': [
    ('What time will the sunrise ride depart?', 'The operating start time and departure point must be confirmed by Nova before this proposed activity is published or booked.'),
    ('Does the sunrise ride include breakfast?', 'Breakfast or other refreshments are included only if expressly listed in your confirmed quote. Sunrise visibility and wildlife sightings cannot be guaranteed.')],
 'full-lake-explorer': [
    ('What makes the extended explorer different from a private charter?', 'This proposed experience needs a defined route and itinerary through different lake settings. It should be published only once Nova verifies that route and the operational arrangements.'),
    ('Does the explorer include Crescent Island admission?', 'Attraction admission is included only if expressly bundled into the selected option and confirmed quote. Check any mandatory separate charges before booking.')],
}


def forwards(apps, schema_editor):
    Tour = apps.get_model('tours','Tour')
    FAQ = apps.get_model('tours','ActivityFAQ')
    for slug, questions in QUESTIONS.items():
        tour = Tour.objects.filter(slug=slug).first()
        if not tour:
            continue
        for order, (question,answer) in zip([1,6],questions):
            FAQ.objects.update_or_create(tour=tour, order=order, defaults={'question':question,'answer':answer})


class Migration(migrations.Migration):
    dependencies = [('tours','0004_activity_catalogue')]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
