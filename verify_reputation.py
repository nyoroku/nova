import os
import django
from django.test import Client

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

def verify():
    client = Client()
    
    # 1. Leaderboard
    print("Verifying Leaderboard...")
    response = client.get('/crew/leaderboard/')
    content = response.content.decode('utf-8')
    if 'Crew Wall of Fame' in content and 'Captain James' in content:
        print("  SUCCESS: Leaderboard displays ranked staff.")
    else:
        print("  FAILURE: Leaderboard issues.")

    # 2. Staff Profile & QR
    print("\nVerifying Staff Profile (James)...")
    response = client.get('/crew/captain-james/')
    content = response.content.decode('utf-8')
    if 'Personal Review Code' in content and 'qr_captain-james.png' in content:
        print("  SUCCESS: Profile page and QR code found.")
    else:
        print("  FAILURE: Profile page issues.")

    # 3. Smart Funnel (Rating)
    print("\nVerifying Smart Funnel - Low Rating...")
    response = client.post('/crew/captain-james/rate/', {
        'customer_name': 'Test User',
        'rating': '2',
        'testimonial_text': 'Bad trip'
    })
    # Follow redirect to success
    response = client.get(response.url)
    content = response.content.decode('utf-8')
    if 'How can we improve?' in content:
        print("  SUCCESS: Low rating funneled to private feedback.")
    else:
        print("  FAILURE: Low rating funnel failed.")

    print("\nVerifying Smart Funnel - High Rating...")
    response = client.post('/crew/captain-james/rate/', {
        'customer_name': 'Best User',
        'rating': '5',
        'testimonial_text': 'Amazing trip thanks!'
    })
    response = client.get(response.url)
    content = response.content.decode('utf-8')
    if 'Paste Review on Google' in content and 'Amazing trip thanks!' in content:
        print("  SUCCESS: High rating funneled to Google Review prompt.")
    else:
        print("  FAILURE: High rating funnel failed.")

if __name__ == "__main__":
    verify()
