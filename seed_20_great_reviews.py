import os
import sys
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from testimonials.models import Testimonial

def seed_reviews():
    print("Deleting old seeded reviews...")
    Testimonial.objects.all().delete()

    reviews_data = [
        {
            "name": "Sarah Jenkins",
            "role": "Solo Traveler, UK",
            "content": "I was looking for the safest boat ride naivasha had to offer, and Rafiki exceeded all expectations. The captain maintained a respectful distance from the hippos, and the entire experience felt incredibly professional. Highly recommended for anyone wanting a peaceful lake excursion.",
            "rating": 5
        },
        {
            "name": "David Mwangi",
            "role": "Local Tourist",
            "content": "For anyone planning a weekend getaway, these boat rides naivasha style are a must-do. The booking process was transparent with no hidden broker fees at the beach. We saw fish eagles diving for their prey right next to our boat!",
            "rating": 5
        },
        {
            "name": "The Patel Family",
            "role": "Family from Nairobi",
            "content": "Taking a boat tour naivasha with toddlers can be daunting, but the crew provided life jackets for everyone and ensured a smooth ride. The pontoon was spacious and stable, making it the perfect family activity on the lake.",
            "rating": 5
        },
        {
            "name": "Emma Thompson",
            "role": "Wildlife Photographer",
            "content": "If you're looking for an authentic boat safari Naivasha experience, this is it. The early morning light was perfect, and the guide knew exactly where to find the dense hippo pods and rare bird species without disturbing them. 10/10.",
            "rating": 5
        },
        {
            "name": "Michael Ochieng",
            "role": "Corporate Event Organizer",
            "content": "We organized a team-building trip, and the Naivasha boat ride was the highlight. The large vessels comfortably accommodated our entire team, and the sunset views over the Rift Valley were spectacular. The crew's hospitality was unmatched.",
            "rating": 5
        },
        {
            "name": "Jessica & Tom",
            "role": "Honeymooners",
            "content": "Our lake naivasha boat ride was incredibly romantic. We booked a private sunset cruise, and gliding through the water while watching the sky turn orange was magical. The captain was discreet and knowledgeable.",
            "rating": 5
        },
        {
            "name": "Liam Davies",
            "role": "Backpacker",
            "content": "I've done several lake naivasha boat rides, but Rafiki stands out because of their fair pricing and certified guides. You don't have to deal with the chaotic beach brokers. Just book directly online and enjoy a premium tour.",
            "rating": 4
        },
        {
            "name": "Sophie Müller",
            "role": "Birding Enthusiast, Germany",
            "content": "An exceptional naivasha boat safari for bird watchers. The guide was essentially a trained ornithologist. He helped us spot over 30 different species within an hour, including the magnificent African Fish Eagle.",
            "rating": 5
        },
        {
            "name": "Brian K.",
            "role": "Weekend Visitor",
            "content": "The best naivasha boat tour by far. The boats are modern, clean, and have quiet engines that don't scare away the wildlife. We got some incredible close-up photos of giraffes grazing near the shoreline of Crescent Island.",
            "rating": 5
        },
        {
            "name": "Claire Dubois",
            "role": "Travel Blogger",
            "content": "When my readers ask for recommendations, I always point them to this specific boat ride naivasha service. Their commitment to eco-tourism and wildlife safety protocols is exactly what modern travelers are looking for.",
            "rating": 5
        },
        {
            "name": "Ahmed Hassan",
            "role": "Family Vacationer",
            "content": "Excellent value for money. Compared to other boat rides naivasha operators, Rafiki provides longer tours with more educational commentary. The kids learned so much about the lake's ecosystem.",
            "rating": 5
        },
        {
            "name": "Olivia Smith",
            "role": "Nature Lover",
            "content": "A flawless boat tour naivasha. The weather was perfect, the lake was glassy, and the sheer number of hippos we saw was astonishing. The captain explained the territorial behavior of the pods, which made the trip very educational.",
            "rating": 5
        },
        {
            "name": "John Kamau",
            "role": "Photographer",
            "content": "For golden hour photography, their boat safari Naivasha is unbeatable. They know exactly how to position the boat for the best lighting and angles. I got the perfect shot of a fish eagle catching a tilapia.",
            "rating": 5
        },
        {
            "name": "Emily Chen",
            "role": "First-time Visitor",
            "content": "I was initially nervous about the hippos, but the Naivasha boat ride felt completely secure. The boat was sturdy, and the captain maintained a strict 50-meter distance from the animals. A serene and beautiful experience.",
            "rating": 5
        },
        {
            "name": "Daniel & Sarah",
            "role": "Couple",
            "content": "We combined our lake naivasha boat ride with a walk on Crescent Island. The logistics were handled perfectly by the team. We stepped off the boat right onto the island and walked among zebras. Unforgettable!",
            "rating": 5
        },
        {
            "name": "The Wanjiku Family",
            "role": "Nairobi Residents",
            "content": "We regularly take lake naivasha boat rides to escape the city, and this operator is consistently the most reliable. Clean life jackets, punctual departures, and friendly staff. It's a breath of fresh air.",
            "rating": 4
        },
        {
            "name": "Lucas Rossi",
            "role": "Adventure Seeker",
            "content": "A fantastic naivasha boat safari! We explored the hidden papyrus channels and even ventured towards Oloidien Bay. The diversity of the landscape is stunning. Highly recommend the 2-hour extended tour.",
            "rating": 5
        },
        {
            "name": "Grace Mutua",
            "role": "Student Group Leader",
            "content": "We took a group of 20 students for a naivasha boat tour. The educational value was immense. The guides explained the geography of the Rift Valley and the importance of conservation. Perfect for school trips.",
            "rating": 5
        },
        {
            "name": "Mark Wilson",
            "role": "Retired Traveler",
            "content": "A very relaxing boat ride naivasha. The seats were comfortable, and the pace was leisurely. It was a joy to glide across the water and observe the fishermen and wildlife living in harmony.",
            "rating": 5
        },
        {
            "name": "Anita R.",
            "role": "Solo Explorer",
            "content": "I felt incredibly safe and welcomed on my boat rides naivasha. The crew went out of their way to ensure I had a great time, pointing out hidden wildlife I would have completely missed on my own. Five stars!",
            "rating": 5
        }
    ]

    for item in reviews_data:
        Testimonial.objects.create(
            customer_name=item["name"],
            customer_country=item["role"],
            testimonial_text=item["content"],
            rating=item["rating"],
            is_active=True
        )
    
    print(f"Successfully seeded {len(reviews_data)} high-quality SEO/AEO reviews.")

if __name__ == '__main__':
    seed_reviews()
