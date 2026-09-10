import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import SiteSettings
from tours.models import Tour
from partners.models import HotelPartner
from stays.models import AccommodationProperty
from packages.models import Package
from bookings.models import BookingLead
from content.models import GuideArticle, QuestionAnswer

def run_tests():
    c = Client()
    print("========================================")
    print("NOVA BOAT RIDES NAIVASHA - TEST SUITE")
    print("========================================")

    failures = 0
    passed = 0

    def assert_status(url, expected_code, name, check_text=None):
        nonlocal failures, passed
        response = c.get(url)
        if response.status_code != expected_code:
            print(f"[FAIL] {name}: GET {url} returned {response.status_code}, expected {expected_code}")
            failures += 1
            return False
        if check_text and check_text not in response.content.decode('utf-8'):
            print(f"[FAIL] {name}: GET {url} content missing expected snippet: '{check_text}'")
            failures += 1
            return False
        print(f"[PASS] {name}: GET {url} -> {response.status_code}")
        passed += 1
        return True

    # 1. Core pages
    assert_status('/', 200, "Home Page", "Naivasha starts here")
    assert_status('/about/', 200, "About Page", "About Nova")
    assert_status('/prices/', 200, "Prices Page", "Transparent Pricing")
    assert_status('/plan-naivasha/', 200, "Plan Naivasha Page", "Optimal Lake Timing")
    assert_status('/contact/', 200, "Contact Page", "Launch Base")

    # 2. Tours
    assert_status('/boat-rides/', 200, "Tour List", "Signature Boat Rides")
    tour = Tour.objects.filter(is_active=True).first()
    if tour:
        assert_status(f'/boat-rides/{tour.slug}/', 200, f"Tour Detail ({tour.slug})", tour.name)
        assert_status(f'/boat-rides/{tour.slug}/quote-partial/?adults=2&children=0&resident_type=RESIDENT', 200, "Tour Quoter Partial", "Calculated Quote")

    # 3. Partners
    assert_status('/hotel-boat-rides/', 200, "Hotel Hub", "Boat Rides from Your Hotel")
    assert_status('/hotel-boat-rides/check/?custom_hotel_name=Great+Rift+Cottages', 200, "Hotel Checker Partial", "Custom Location Check")
    
    # Check Sopa reference rule (must return 404 because public_page_enabled=False)
    sopa = HotelPartner.objects.filter(slug='lake-naivasha-sopa-resort').first()
    if sopa:
        assert_status('/hotel-boat-rides/lake-naivasha-sopa-resort/', 404, "Sopa Reference Gate (Must 404)")

    # Check active public partner
    enashipai = HotelPartner.objects.filter(slug='enashipai-resort-spa', public_page_enabled=True).first()
    if enashipai:
        assert_status('/hotel-boat-rides/enashipai-resort-spa/', 200, "Enashipai Detail", "Enashipai")

    # 4. Stays
    assert_status('/stay/', 200, "Stay List", "Where to Stay in Naivasha")
    stay = AccommodationProperty.objects.filter(is_active=True).first()
    if stay:
        assert_status(f'/stay/{stay.slug}/', 200, f"Stay Detail ({stay.slug})", stay.name)

    # 5. Packages
    assert_status('/packages/', 200, "Package List", "Stay + Ride Packages")
    pkg = Package.objects.filter(is_active=True).first()
    if pkg:
        assert_status(f'/packages/{pkg.slug}/', 200, f"Package Detail ({pkg.slug})", pkg.name)
        assert_status(f'/packages/{pkg.slug}/quote-partial/?adults=2&children=0', 200, "Package Quoter Partial", "Package Estimate Breakdown")

    # 6. Bookings
    assert_status('/book/', 200, "Book Form GET", "Reservation Request")
    
    # Test POST submission via HTMX
    post_data = {
        'lead_type': 'BOAT_ONLY',
        'tour': tour.pk if tour else 1,
        'preferred_date': '2026-09-15',
        'preferred_time': 'MORNING_0830',
        'adults': 2,
        'children': 1,
        'transport_required': 'NONE',
        'guest_name': 'Sarah Jenkins',
        'guest_phone': '+254711223344',
        'guest_email': 'sarah@example.com',
        'consent_operational': True,
    }
    resp = c.post('/book/', post_data, HTTP_HX_REQUEST='true')
    if resp.status_code == 200 and "You're Almost on the Water!" in resp.content.decode('utf-8'):
        print("[PASS] Book Form POST (HTMX) -> 200 and Success Partial")
        passed += 1
    else:
        print(f"[FAIL] Book Form POST (HTMX) -> status {resp.status_code}")
        failures += 1

    # Verify BookingLead was saved in database
    lead = BookingLead.objects.filter(guest_name='Sarah Jenkins').last()
    if lead and lead.quoted_total_amount > 0 and lead.reference_number:
        print(f"[PASS] Lead Persisted in DB: Ref #{lead.reference_number}, Quoted Total: KES {lead.quoted_total_amount}")
        passed += 1
    else:
        print("[FAIL] Lead failed to persist or quoted amount is missing")
        failures += 1

    # 7. Content (Journal & FAQs)
    assert_status('/journal/', 200, "Journal List", "Lake Guides & Field Notes")
    art = GuideArticle.objects.filter(is_active=True).first()
    if art:
        assert_status(f'/journal/{art.slug}/', 200, f"Journal Detail ({art.slug})", "Lake Naivasha")
    assert_status('/questions/', 200, "FAQ List", "Lake Questions & Direct Answers")

    # 8. Sitemaps
    assert_status('/sitemap.xml', 200, "Sitemap Index")
    assert_status('/sitemap-static.xml', 200, "Static Sitemap")
    assert_status('/sitemap-tours.xml', 200, "Tours Sitemap")
    assert_status('/sitemap-hotels.xml', 200, "Hotels Sitemap")
    assert_status('/sitemap-stays.xml', 200, "Stays Sitemap")
    assert_status('/sitemap-packages.xml', 200, "Packages Sitemap")
    assert_status('/sitemap-guides.xml', 200, "Guides Sitemap")

    # 9. Legacy 301 Redirects
    redirect_tests = [
        ('/tours/', '/boat-rides/'),
        ('/accommodation/', '/stay/'),
        ('/reviews/', '/about/'),
        ('/faq/', '/questions/'),
    ]
    for src, dst in redirect_tests:
        r = c.get(src)
        if r.status_code == 301 and r.url == dst:
            print(f"[PASS] Legacy 301: {src} -> {dst}")
            passed += 1
        else:
            print(f"[FAIL] Legacy 301: {src} returned {r.status_code} -> {r.url if hasattr(r, 'url') else 'none'}")
            failures += 1

    print("----------------------------------------")
    print(f"URL & LOGIC TESTS COMPLETE: {passed} PASSED, {failures} FAILED.")
    print("========================================")

    # 10. Brand Residue Regression Scan
    print("\nRUNNING BRAND RESIDUE REGRESSION SCAN...")
    residue_patterns = [
        "Rafiki", "rafiki",
        "729 280 380", "729280380",
        "700 000 000", "700000000",
        "hello@rafikiboatridesnaivasha.com",
        "rafikiboatridesnaivasha.com"
    ]
    
    scan_dirs = ['templates', 'core', 'tours', 'partners', 'stays', 'packages', 'bookings', 'content', 'seo']
    residue_found = 0

    for d in scan_dirs:
        for root, dirs, files in os.walk(d):
            if 'migrations' in root or 'quarantine' in root:
                continue
            for file in files:
                if file.endswith(('.html', '.py', '.css', '.js')):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for idx, line in enumerate(lines, 1):
                            for pat in residue_patterns:
                                if pat in line:
                                    if "legacy" in line.lower() or "rafiki reference" in line.lower():
                                        continue
                                    print(f"  [RESIDUE WARNING] {filepath}:{idx} contains '{pat}': {line.strip()[:60]}")
                                    residue_found += 1

    if residue_found == 0:
        print("[PASS] BRAND INTEGRITY VERIFIED: ZERO UNWANTED BRAND RESIDUES IN CODEBASE!")
    else:
        print(f"[WARN] Found {residue_found} potential residue instances. Review above.")

if __name__ == '__main__':
    run_tests()
