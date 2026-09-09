import os
import shutil
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG = os.path.join(BASE_DIR, 'static', 'images')
NOVA_IMG = os.path.join(STATIC_IMG, 'nova')
os.makedirs(NOVA_IMG, exist_ok=True)

MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Source files from canonical static/images/nova/
SOURCES = {
    'captain_family': os.path.join(NOVA_IMG, 'captain_family.jpg'),
    'crescent_ostrich': os.path.join(NOVA_IMG, 'crescent_ostrich.jpg'),
    'lake_cruise': os.path.join(NOVA_IMG, 'lake_cruise.jpg'),
    'giraffes': os.path.join(NOVA_IMG, 'giraffes.jpg')
}

def save_variants(src_path, target_base_without_ext, max_w=1024, mobile_w=480):
    im = Image.open(src_path).convert('RGB')
    
    # Master WebP & formats
    w, h = im.size
    if w > max_w:
        ratio = max_w / float(w)
        h_new = int(float(h) * float(ratio))
        im_large = im.resize((max_w, h_new), Image.Resampling.LANCZOS)
    else:
        im_large = im.copy()
        
    os.makedirs(os.path.dirname(target_base_without_ext), exist_ok=True)
    im_large.save(f"{target_base_without_ext}.webp", 'WEBP', quality=85, method=6)
    im_large.save(f"{target_base_without_ext}.jpg", 'JPEG', quality=85)
    im_large.save(f"{target_base_without_ext}.png", 'PNG', optimize=True)
    
    # Mobile WebP
    ratio_m = mobile_w / float(w)
    h_m = int(float(h) * float(ratio_m))
    im_mobile = im.resize((mobile_w, h_m), Image.Resampling.LANCZOS)
    im_mobile.save(f"{target_base_without_ext}_mobile.webp", 'WEBP', quality=80, method=6)

def run():
    print("=== PROCESSING AND REPLACING ALL PROJECT IMAGES ===")
    
    # 1. Replace static/images/ keys
    # Lake Cruise Scenic -> hero_sunset, hero_main_v2, hero
    save_variants(SOURCES['lake_cruise'], os.path.join(STATIC_IMG, 'hero_sunset'))
    save_variants(SOURCES['lake_cruise'], os.path.join(STATIC_IMG, 'hero_main_v2'))
    save_variants(SOURCES['lake_cruise'], os.path.join(STATIC_IMG, 'hero'))
    
    # Captain & Family -> hero_local
    save_variants(SOURCES['captain_family'], os.path.join(STATIC_IMG, 'hero_local'))
    
    # Crescent Island Ostrich & Guest -> hero_crescent, crescent_girl, crescent_ostrich, crescent_zebra, crescent_wildebeest, crescent_monkey
    crescent_keys = ['hero_crescent', 'crescent_girl', 'crescent_ostrich', 'crescent_zebra', 'crescent_wildebeest', 'crescent_monkey']
    for ck in crescent_keys:
        save_variants(SOURCES['crescent_ostrich'], os.path.join(STATIC_IMG, ck))
        
    # Giraffes Wildlife -> hero_wildlife, hero_birds
    wildlife_keys = ['hero_wildlife', 'hero_birds']
    for wk in wildlife_keys:
        save_variants(SOURCES['giraffes'], os.path.join(STATIC_IMG, wk))
        
    # 2. Generate fresh Favicon from Lake Cruise
    im_fav = Image.open(SOURCES['lake_cruise']).convert('RGBA')
    min_dim = min(im_fav.size)
    left = (im_fav.width - min_dim) // 2
    top = (im_fav.height - min_dim) // 2
    im_fav_sq = im_fav.crop((left, top, left + min_dim, top + min_dim))
    im_fav_sq.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(STATIC_IMG, 'favicon.ico'), format='ICO')
    print("[OK] Re-generated favicon.ico from Lake Cruise image.")

    # 3. Remove Legacy unneeded folders in static/images
    for old_dir in ['rafiki-august', 'rafiki-gallery']:
        full_old = os.path.join(STATIC_IMG, old_dir)
        if os.path.exists(full_old):
            shutil.rmtree(full_old)
            print(f"[REMOVED] Legacy folder: {old_dir}")
            
    for old_file in ['icon.jpg', 'logos.jpg', 'njoviclogo.jpg', 'njoviclogo.png']:
        full_old = os.path.join(STATIC_IMG, old_file)
        if os.path.exists(full_old):
            os.remove(full_old)
            print(f"[REMOVED] Legacy image file: {old_file}")

    # 4. Populate media/ with organized domain folders
    media_folders = ['tours', 'tours/webp', 'stays', 'stays/webp', 'packages', 'packages/webp', 
                     'partners', 'partners/webp', 'crew', 'crew/webp', 'journal', 'journal/webp', 'testimonials']
    for mf in media_folders:
        os.makedirs(os.path.join(MEDIA_DIR, mf), exist_ok=True)
        
    # Generate media items
    # Tours:
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'tours', 'classic-lake-safari'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'tours', 'hippo-bird-safari'))
    save_variants(SOURCES['crescent_ostrich'], os.path.join(MEDIA_DIR, 'tours', 'crescent-island'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'tours', 'sunset-cruise'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'tours', 'family-cruise'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'tours', 'photography-birding'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'tours', 'groups-events'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'tours', 'private-charter'))
    
    # Stays:
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'stays', 'lake-naivasha-sopa-resort'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'stays', 'enashipai-resort-spa'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'stays', 'kiboko-luxury-camp'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'stays', 'camp-carnelleys-cottages'))
    
    # Packages:
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'packages', 'stay-and-ride'))
    save_variants(SOURCES['crescent_ostrich'], os.path.join(MEDIA_DIR, 'packages', 'crescent-island-safari'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'packages', 'sunset-safari'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'packages', 'family-safari'))
    
    # Partners:
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'partners', 'enashipai-resort-spa'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'partners', 'kiboko-luxury-camp'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'partners', 'lake-naivasha-sopa-resort'))
    
    # Crew (Lead Captain Dennis Maina):
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'crew', 'captain-dennis-maina'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'crew', 'captain-peter-kariuki'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'crew', 'guide-samuel-ndungu'))

    # Journal:
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'journal', 'nairobi-to-naivasha-guide'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'journal', 'lake-naivasha-hippo-safety'))
    save_variants(SOURCES['crescent_ostrich'], os.path.join(MEDIA_DIR, 'journal', 'crescent-island-walking-guide'))

    # Testimonials:
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'testimonials', 'sarah-mark'))
    save_variants(SOURCES['captain_family'], os.path.join(MEDIA_DIR, 'testimonials', 'david-family'))
    save_variants(SOURCES['giraffes'], os.path.join(MEDIA_DIR, 'testimonials', 'elena-marcus'))
    save_variants(SOURCES['lake_cruise'], os.path.join(MEDIA_DIR, 'testimonials', 'kigali-team'))

    # Clean old legacy folders in media
    for old_m in ['tour_images', 'location_images', 'service_images', 'blog_images', 'testimonial_photos', 'hotel_images', 'location_gallery', 'staff_qr_codes', 'hotel_gallery']:
        p = os.path.join(MEDIA_DIR, old_m)
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"[REMOVED] Legacy media directory: {old_m}")

    print("=== IMAGE PROCESSING COMPLETE ===")

if __name__ == '__main__':
    run()
