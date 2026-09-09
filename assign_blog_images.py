import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from blog.models import Post
from django.conf import settings

# Source paths
sources = {
    1: r"C:/Users/Administrator/.gemini/antigravity/brain/b17d6bef-0d2e-4086-b993-3f13be745b17/kenya_adventure_blog_1769939407695.png",
    2: r"C:/Users/Administrator/.gemini/antigravity/brain/b17d6bef-0d2e-4086-b993-3f13be745b17/naivasha_guide_blog_1769939433974.png",
    3: r"C:/Users/Administrator/.gemini/antigravity/brain/b17d6bef-0d2e-4086-b993-3f13be745b17/guru_adventures_blog_1769939450139.png"
}

# Target directory
target_dir = os.path.join(settings.MEDIA_ROOT, 'blog_images')
os.makedirs(target_dir, exist_ok=True)

for post_id, src_path in sources.items():
    if os.path.exists(src_path):
        filename = os.path.basename(src_path)
        dest_path = os.path.join(target_dir, filename)
        
        # Copy file
        shutil.copy2(src_path, dest_path)
        print(f"Copied {filename} to {dest_path}")
        
        # Update database
        try:
            post = Post.objects.get(id=post_id)
            post.image = f"blog_images/{filename}"
            post.save()
            print(f"Updated Post {post_id}: {post.title}")
        except Post.DoesNotExist:
            print(f"Post {post_id} not found.")
    else:
        print(f"Source file not found: {src_path}")
