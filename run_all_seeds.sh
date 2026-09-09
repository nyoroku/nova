#!/bin/bash
# ============================================================
# KATRUE — Full Database Seeder
# Run on PythonAnywhere Bash Console:
#   bash run_all_seeds.sh
# ============================================================

set -e  # Stop on any error

# Detect environment and set directories
if [ -d "/home/rafikiboats/rafiki" ]; then
    PROJECT_DIR="/home/rafikiboats/rafiki"
    VENV_ACTIVATE="/home/rafikiboats/venv/bin/activate"
else
    PROJECT_DIR="c:/rafiki"
    VENV_ACTIVATE="c:/rafiki/.venv/Scripts/activate"
fi

cd "$PROJECT_DIR"
source "$VENV_ACTIVATE"

echo ""
echo "============================================================"
echo " KATRUE FULL SEEDER — STARTING"
echo "============================================================"
echo ""

# --- STEP 1: Core site data ---
echo "[1/9] Seeding core site data..."
python seed_katrue.py
python seed_site.py

# --- STEP 2: First wave FAQs & Local Pages ---
echo "[2/9] Seeding first wave SEO content..."
python seed_seo_content.py
python seed_faqs_pages.py

# --- STEP 3: FAQ batches (4 thematic domains) ---
echo "[3/9] Seeding FAQ batches (Logistics, Wildlife, Geography, Safety)..."
python seed_faq_batch1_logistics.py
python seed_faq_batch2_wildlife.py
python seed_faq_batch3_geography.py
python seed_faq_batch4_safety.py

# --- STEP 4: Pillar blog posts (20 batches) ---
echo "[4/9] Seeding pillar blog posts..."
python seed_pillar_blogs.py
python seed_pillar_batch1.py
python seed_pillar_batch2.py
python seed_pillar_batch3.py
python seed_pillar_batch4.py
python seed_pillar_batch5.py
python seed_pillar_batch6.py
python seed_pillar_batch7.py
python seed_pillar_batch8.py
python seed_pillar_batch9.py
python seed_pillar_batch10.py
python seed_pillar_batch11.py
python seed_pillar_batch12.py
python seed_pillar_batch13.py
python seed_pillar_batch14.py
python seed_pillar_batch15.py
python seed_pillar_batch16.py
python seed_pillar_batch17.py
python seed_pillar_batch18.py
python seed_pillar_batch19.py
python seed_pillar_batch20.py

# --- STEP 5: Bulk blogs & programmatic SEO routes ---
echo "[5/9] Seeding bulk blogs and pSEO routes..."
python seed_blogs_bulk.py
python seed_pseo_routes.py

# --- STEP 6: Funnel SEO & Phase 9 local pages ---
echo "[6/9] Seeding funnel SEO and Phase 9 local pages..."
python seed_funnel_seo.py
python seed_phase9_local_pages.py

# --- STEP 7: Phase 10 additional FAQs ---
echo "[7/9] Seeding Phase 10 FAQs..."
python seed_phase10_faqs.py

# --- STEP 8: Scale and target strategic niches ---
echo "[8/9] Scaling to 500+ items and targeting strategic niches..."
python seed_phase11_500_faqs.py
python seed_phase12_500_local_pages.py
python seed_phase13_500_blogs.py
python seed_faq_topup.py
python seed_growth_blogs.py

# --- STEP 9: Final verification ---
echo ""
echo "[9/9] Final count verification..."
python - <<'EOF'
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
sys.path.insert(0, '.')
django.setup()
from blog.models import Post
from seo.models import FAQ, LocalPage

faqs   = FAQ.objects.filter(is_active=True).count()
pages  = LocalPage.objects.filter(is_active=True).count()
blogs  = Post.objects.count()

print()
print("============================================================")
print(" KATRUE SEEDING COMPLETE — FINAL STATUS")
print("============================================================")
print(f"  FAQs (active):        {faqs:>4} / 500  {'✓' if faqs >= 500 else '✗ NEEDS MORE'}")
print(f"  Local Pages (active): {pages:>4} / 1000 {'✓' if pages >= 1000 else '✗ NEEDS MORE'}")
print(f"  Blog Posts (total):   {blogs:>4} / 600  {'✓' if blogs >= 600 else '✗ NEEDS MORE'}")
print("============================================================")
EOF

echo ""
echo "Done."
