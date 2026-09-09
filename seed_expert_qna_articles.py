import os
import django
from django.utils.text import slugify
from django.core.files import File
from pathlib import Path

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "static" / "images"

def seed_qna_articles():
    print("=== Seeding Long Expert Q&A Articles ===")
    
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@rafikiboatride.com', 'AdminPass123!')
        print("Created superuser 'admin'")

    articles = [
        {
            "title": "The Ultimate Guide to a Lake Naivasha Boat Ride (Logistics, Pricing & Hippo Safety)",
            "meta_description": "Planning a naivasha boat ride? Read our expert Q&A guide on prices, booking a private boatride, spotting hippos, and timing your Lake Naivasha boat trip.",
            "image_file": "crescent_girl.webp",
            "content": """
<h2>The Ultimate Guide to a Lake Naivasha Boat Ride</h2>
<p>If you are planning a weekend trip or holiday in Kenya, a <strong>lake naivasha boat ride</strong> is likely at the top of your list. To help you plan, our local captains have compiled this expert Q&A guide covering everything from prices to hippo safety.</p>

<div class="my-4">
    <img src="/static/images/crescent_girl.webp" alt="Tourist enjoying a private boatride to Crescent Island" class="rounded shadow img-fluid w-100" style="max-height: 450px; object-fit: cover;">
</div>

<h3>Q: What should I expect on a standard lake naivasha boat tour?</h3>
<p><strong>A:</strong> A typical <strong>lake naivasha boat tour</strong> is a private, guided safari conducted in motorized speedboats or spacious pontoon boats. The tour takes you through shallow papyrus-fringed channels where you will see nesting African Fish Eagles, diving kingfishers, pelicans, and large pods of hippos resting in the water. Most tours launch from <strong>Karagita Public Beach</strong> and can include a transfer for a walking safari on Crescent Island.</p>

<h3>Q: How much does a naivasha boat ride cost?</h3>
<p><strong>A:</strong> Unlike municipal transport, a private <strong>boatride</strong> on the lake is charged per boat (seating up to 7 or 8 passengers), rather than per person. For residents, a standard 1.5-hour wildlife safari starts at KES 3,000, while a Crescent Island transfer cruise is KES 4,500. For international tourists, the prices range from $45 USD to $75 USD per boat. Private pontoon charters for large groups are KES 15,000 ($250 USD).</p>

<h3>Q: Is it safe to be near a hippo during the boatride?</h3>
<p><strong>A:</strong> Yes, provided your captain follows strict safety margins. The <strong>hippo</strong> is a highly territorial animal, and they can be aggressive if cornered. Rafiki captains maintain a minimum buffer zone of 50 meters from all hippo pods and navigate at low speeds near the shoreline to avoid disturbing them. All passengers are required to wear certified life jackets throughout the <strong>lake naivasha boat trip</strong>.</p>

<h3>Q: What is the best time of day to plan my boat ride?</h3>
<p><strong>A:</strong> Early morning (6:30 AM to 8:30 AM) is the best time for bird watching and photography, as the waters are calm and the light is soft. Late afternoon (4:30 PM to 6:00 PM) is the ideal time for a sunset cruise, offering dramatic views of the volcanic hills surrounding <strong>naivasha</strong>.</p>
<p>Ready to book your private lake safari? Message Rafiki on WhatsApp: <a href="https://wa.me/254729280380"><strong>+254 729 280 380</strong></a>.</p>
            """,
            "tags": ["lake naivasha boat ride", "boatride", "hippo", "naivasha boat ride"]
        },
        {
            "title": "Romantic Places to Visit in Naivasha (The Perfect Couple's Guide)",
            "meta_description": "Looking for romantic places to visit in naivasha? Read our expert Q&A on sunset cruises, walking safaris, and planning a romantic lake naivasha boat tour.",
            "image_file": "crescent_zebra.webp",
            "content": """
<h2>Romantic Places to Visit in Naivasha</h2>
<p>With its beautiful yellow fever trees, volcanic backdrops, and peaceful waters, the lake is one of the most popular weekend getaways for couples. Here is our expert guide to the most <strong>romantic places to visit in naivasha</strong>.</p>

<div class="my-4">
    <img src="/static/images/crescent_zebra.webp" alt="Zebras grazing on Crescent Island shores" class="rounded shadow img-fluid w-100" style="max-height: 450px; object-fit: cover;">
</div>

<h3>Q: Why is Crescent Island considered one of the top romantic spots in naivasha?</h3>
<p><strong>A:</strong> Crescent Island is a private sanctuary where you can step off your boat and walk hand-in-hand directly next to zebras, giraffes, and waterbucks. Because there are no predators, it is peaceful and romantic. The island offers panoramic views of the entire lake and the surrounding Rift Valley hills.</p>

<h3>Q: What is the most romantic lake naivasha boat tour experience?</h3>
<p><strong>A:</strong> The <strong>Sunset Cruise</strong> is the ultimate couple's experience. Launching at 5:00 PM, this private <strong>lake naivasha boat trip</strong> takes you out to the open waters as the sun goes down, casting a golden glow over the water. Many couples choose this tour for proposals, anniversary celebrations, or quiet evening photography.</p>

<h3>Q: How do we combine a romantic stay with a naivasha boat ride?</h3>
<p><strong>A:</strong> We recommend booking a room at one of the luxury partner lodges along the shores, such as Enashipai Resort & Spa or Lake Naivasha Sopa Resort. Rafiki can arrange to pick you up directly from the hotel's private pier for your private boat ride, making the transition seamless and private.</p>

<h3>Q: Do we need to book our couple's boatride in advance?</h3>
<p><strong>A:</strong> While walk-ins are available, we highly recommend booking in advance via WhatsApp to guarantee a private boat and customize your itinerary (such as adding a surprise setup, a bottle of wine, or a specific sunset route).</p>
<p>Plan your romantic weekend safari with Rafiki: WhatsApp <a href="https://wa.me/254729280380"><strong>+254 729 280 380</strong></a>.</p>
            """,
            "tags": ["romantic places to visit in naivasha", "lake naivasha boat tour", "naivasha"]
        },
        {
            "title": "Freshwater Angling in the Rift Valley: Where to Fish & Lake Naivasha Guides",
            "meta_description": "Searching for the best places to fish near me? Read our expert Q&A on freshwater sport fishing on Lake Naivasha, catch species, and booking a boat trip.",
            "image_file": "crescent_wildebeest.webp",
            "content": """
<h2>Freshwater Angling in the Rift Valley: Best Places to Fish</h2>
<p>If you are an angler visiting Kenya or a local resident searching online for the <strong>best places to fish near me</strong>, Lake Naivasha stands out as the premier freshwater fishery in the southern Rift Valley. Here is our expert guide on where to fish, what you will catch, and how to book a guided trip.</p>

<div class="my-4">
    <img src="/static/images/crescent_wildebeest.webp" alt="Wildlife on the shores of Lake Naivasha" class="rounded shadow img-fluid w-100" style="max-height: 450px; object-fit: cover;">
</div>

<h3>Q: Why is Lake Naivasha ranked among the best places to fish near me?</h3>
<p><strong>A:</strong> Lake Naivasha is a large freshwater lake populated by Nile Tilapia, Largemouth Bass, and Common Carp. Unlike the salty Rift Valley lakes, Naivasha's ecosystem supports rich fish populations, making it highly productive for both recreational sport fishing and local commercial fishing.</p>

<h3>Q: How do I book a guided fishing trip on the lake?</h3>
<p><strong>A:</strong> You can book a dedicated <strong>Sport Fishing Safari</strong> boat ride with Rafiki. We provide motorized boats, standard spinning rods, reels, and bait. Your captain will navigate to the most productive shallow bays and papyrus margins where largemouth bass hunt for food.</p>

<h3>Q: What is the cost of a fishing lake naivasha boat ride?</h3>
<p><strong>A:</strong> A guided 3-hour sport fishing <strong>lake naivasha boat trip</strong> costs KES 6,000 for residents ($100 USD for international guests). This price includes the boat hire, a local captain who knows the best fishing grounds, and standard rods and bait for up to 4 anglers.</p>

<h3>Q: What is the best season and time of day for fishing in naivasha?</h3>
<p><strong>A:</strong> Early morning (6:30 AM to 9:00 AM) and late afternoon (4:00 PM to 6:00 PM) are the most active feeding times. In terms of seasons, the transition periods after the rainy seasons (June-July and December-January) often yield the highest catch rates as water levels stabilize.</p>
<p>Book your guided fishing safari: WhatsApp Rafiki at <a href="https://wa.me/254729280380"><strong>+254 729 280 380</strong></a>.</p>
            """,
            "tags": ["best places to fish near me", "lake naivasha boat ride", "naivasha boat ride", "naivasha"]
        }
    ]

    for article in articles:
        slug = slugify(article["title"])
        post, created = Post.objects.update_or_create(
            slug=slug,
            defaults={
                "title": article["title"],
                "author": admin,
                "content": article["content"],
                "meta_description": article["meta_description"],
                "status": "published",
            }
        )
        post.tags.add(*article["tags"])
        
        # Attach featured image
        img_filename = article["image_file"]
        static_img_path = IMAGE_DIR / img_filename
        if static_img_path.exists():
            with static_img_path.open("rb") as handle:
                post.image.save(img_filename, File(handle), save=False)
            post.save()
            print(f"Seeded expert article: {post.title} (Created: {created}) with featured image {img_filename}")
        else:
            print(f"Seeded expert article: {post.title} (Created: {created}) - Warning: Image {img_filename} not found!")

    print("=== Expert Q&A Blogs Seeding Complete ===")

if __name__ == "__main__":
    seed_qna_articles()
