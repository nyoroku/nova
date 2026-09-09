import os
import shutil

# Configurations
OLD_NUM_WA = "254791734268"
NEW_NUM_WA = "254718030511"

OLD_NUM_DISPLAY = "+254 791 734 268"
NEW_NUM_DISPLAY = "+254 718 030 511"

OLD_NUM_TEL = "+254791734268"
NEW_NUM_TEL = "+254718030511"

OLD_NUM_ALTERNATE = "0791 734 268"
NEW_NUM_ALTERNATE = "0718 030 511"

TEMPLATES_DIR = r"c:\Users\Administrator\PycharmProjects\boats\templates"
STATIC_IMAGES_DIR = r"c:\Users\Administrator\PycharmProjects\boats\static\images"
NEW_LOGO_SOURCE = r"C:\Users\Administrator\.gemini\antigravity\brain\4370f9b0-5c16-4a4b-9609-9ea966aef352\uploaded_media_1770034258742.jpg"

def update_templates():
    print("Updating templates...")
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content.replace(OLD_NUM_WA, NEW_NUM_WA)
                new_content = new_content.replace(OLD_NUM_DISPLAY, NEW_NUM_DISPLAY)
                new_content = new_content.replace(OLD_NUM_TEL, NEW_NUM_TEL)
                new_content = new_content.replace(OLD_NUM_ALTERNATE, NEW_NUM_ALTERNATE)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {path}")

def update_assets():
    print("Updating assets...")
    targets = [
        os.path.join(STATIC_IMAGES_DIR, "logos.jpg"),
        os.path.join(STATIC_IMAGES_DIR, "icon.jpg")
    ]
    for target in targets:
        shutil.copy2(NEW_LOGO_SOURCE, target)
        print(f"Replaced: {target}")

if __name__ == "__main__":
    update_templates()
    update_assets()
    print("Done!")
