import shutil
import os

source_dir = r"C:\Users\Administrator\.gemini\antigravity\brain\3d5c856b-c4b2-4c9a-a29e-e8c89103e599"
target_base = r"C:\Users\Administrator\PycharmProjects\boats\media"

mappings = {
    # Services
    'service_nature_education_1769899175206.png': 'service_images/nature_education.png',
    'service_corporate_events_1769899191535.png': 'service_images/corporate_events.png',
    'service_adventure_fishing_1769899206913.png': 'service_images/adventure_fishing.png',
    
    # Destinations
    'dest_boat_rides_1769902550090.png': 'location_images/boat_rides.png',
    'dest_crescent_island_1769902572338.png': 'location_images/crescent_island.png',
    'dest_sunset_cruise_1769902588796.png': 'location_images/sunset_cruise.png',
    'dest_hippo_point_1769903275317.png': 'location_images/hippo_point.png',
    'dest_elsamere_1769903292879.png': 'location_images/elsamere.png',
    
    # Tours (Repurposed)
    'tour_crescent_walking_1769904600336.png': 'tour_images/crescent_walking.png',
    'tour_full_day_adventure_1769904615733.png': 'tour_images/full_day.png',
    'hero_birds_1769889893243.png': 'tour_images/hippo_bird.png',
    'hero_wildlife_1769888612677.png': 'tour_images/photography.png',
    'hero_main_v2_1769889863059.png': 'tour_images/private_charter.png',
    'hero_sunset_1769888628442.png': 'tour_images/sunset_cruise.png',
}

print("Synchronizing media files...")
for src_name, rel_path in mappings.items():
    src = os.path.join(source_dir, src_name)
    dst = os.path.join(target_base, rel_path)
    
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        shutil.copy2(src, dst)
        print(f"[OK] Copied {src_name} to {rel_path}")
    except Exception as e:
        print(f"[ERROR] Failed to copy {src_name}: {e}")

print("Sync complete.")
