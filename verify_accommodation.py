import os
import django
from django.test import Client

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

def verify_pages():
    client = Client()
    
    pages = [
        {'url': '/', 'content': 'Plan Your Stay'},
        {'url': '/accommodation/', 'content': 'Our Partner Hotels'},
        {'url': '/accommodation/naivasha-lakefront-resort/', 'content': 'Naivasha Lakefront Resort'}
    ]
    
    for page in pages:
        print(f"Verifying {page['url']}...")
        response = client.get(page['url'])
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if page['content'] in content:
                print(f"  SUCCESS: Found '{page['content']}'")
            else:
                print(f"  FAILURE: Could not find '{page['content']}'")
        else:
            print(f"  FAILURE: Status code {response.status_code}")

if __name__ == "__main__":
    verify_pages()
