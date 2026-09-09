from decimal import Decimal
from django.db import migrations


def add_combo(apps, schema_editor):
    Tour = apps.get_model("bookings", "Tour")
    Tour.objects.update_or_create(
        slug="hells-gate-boat-combo",
        defaults={
            "name": "Hell's Gate + Lake Naivasha Boat Combo",
            "description": (
                "<p>Make the most of a Naivasha day by combining an active Hell's Gate experience with "
                "a guided boat ride on Lake Naivasha.</p><p>Start with cycling or hiking among the park's "
                "dramatic landscapes, then change pace on the lake while looking for hippos, fish eagles "
                "and shoreline birdlife.</p><p>The final route, transport, bicycle hire and park entry are "
                "confirmed directly for your group before travel.</p>"
            ),
            "seo_title": "Hell's Gate & Lake Naivasha Boat Combo | Rafiki",
            "meta_description": "Combine Hell's Gate cycling or hiking with a guided Lake Naivasha wildlife boat ride in one flexible day experience.",
            "highlights": "Hell's Gate cycling or hiking\nLake Naivasha wildlife boat ride\nFlexible private itinerary\nLocal planning support",
            "location": "Hell's Gate & Lake Naivasha",
            "duration_hours": Decimal("7.0"),
            "price_resident": Decimal("9500.00"),
            "price_international": Decimal("95.00"),
            "max_people": 8,
            "is_active": True,
            "allow_indexing": True,
        },
    )


def remove_combo(apps, schema_editor):
    Tour = apps.get_model("bookings", "Tour")
    Tour.objects.filter(slug="hells-gate-boat-combo").delete()


class Migration(migrations.Migration):
    dependencies = [("bookings", "0005_tour_webp_image_tour_webp_mobile")]
    operations = [migrations.RunPython(add_combo, remove_combo)]
