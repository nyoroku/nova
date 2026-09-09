import os
import shutil
from PIL import Image, ImageDraw

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
    'giraffes': os.path.join(NOVA_IMG, 'giraffes.jpg'),
    'logo_source': os.path.join(NOVA_IMG, 'nova_logo_source.jpg'),
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
        
    # 2. Generate Brand Logo & Multi-Resolution Favicons
    if os.path.exists(SOURCES['logo_source']):
        im_logo = Image.open(SOURCES['logo_source']).convert('RGBA')
        cx, cy = 509.5, 477.5
        r = 254 + 2
        box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
        cropped = im_logo.crop(box)
        w, h = cropped.size

        # Circular mask for antialiased transparency
        scale = 4
        mask = Image.new('L', (w * scale, h * scale), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, w * scale, h * scale), fill=255)
        mask = mask.resize((w, h), Image.Resampling.LANCZOS)

        transparent_logo = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        transparent_logo.paste(cropped, (0, 0), mask=mask)

        # Save logo variants
        logo_512 = transparent_logo.resize((512, 512), Image.Resampling.LANCZOS)
        logo_512.save(os.path.join(STATIC_IMG, 'nova-logo.png'), 'PNG', optimize=True)
        logo_512.save(os.path.join(NOVA_IMG, 'nova-logo.png'), 'PNG', optimize=True)
        logo_512.save(os.path.join(STATIC_IMG, 'nova-logo.webp'), 'WEBP', quality=95, method=6)

        logo_96 = transparent_logo.resize((96, 96), Image.Resampling.LANCZOS)
        logo_96.save(os.path.join(STATIC_IMG, 'nova-logo-96.png'), 'PNG', optimize=True)
        logo_96.save(os.path.join(STATIC_IMG, 'nova-logo-96.webp'), 'WEBP', quality=95)

        # Apple Touch Icon (180x180) on Obsidian background
        apple_icon = Image.new('RGBA', (180, 180), (19, 18, 24, 255))
        logo_160 = transparent_logo.resize((160, 160), Image.Resampling.LANCZOS)
        apple_icon.paste(logo_160, (10, 10), mask=logo_160)
        apple_icon.convert('RGB').save(os.path.join(STATIC_IMG, 'apple-touch-icon.png'), 'PNG')

        # Favicons
        logo_32 = transparent_logo.resize((32, 32), Image.Resampling.LANCZOS)
        logo_32.save(os.path.join(STATIC_IMG, 'favicon-32x32.png'), 'PNG')
        logo_16 = transparent_logo.resize((16, 16), Image.Resampling.LANCZOS)
        logo_16.save(os.path.join(STATIC_IMG, 'favicon-16x16.png'), 'PNG')

        # Multi-resolution ICO
        logo_512.save(os.path.join(STATIC_IMG, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
        print("[OK] Generated brand logo and multi-resolution favicons.")

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
