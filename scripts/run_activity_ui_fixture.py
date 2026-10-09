"""Isolated, clearly labelled UI fixture; never modifies Nova's normal database or media."""
import os
import sys
from pathlib import Path
from io import BytesIO

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
from django.conf import settings

fixture_root = ROOT / 'outputs' / 'activity-rebuild' / 'ui-fixture'
fixture_root.mkdir(parents=True, exist_ok=True)
settings.DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':fixture_root / 'fixture.sqlite3'}}
settings.MEDIA_ROOT = fixture_root / 'media'
import django
django.setup()
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image, ImageDraw
from tours.models import Tour, TourOption, ExperienceRate, ActivityImage
from django.utils import timezone

call_command('migrate', verbosity=0, interactive=False)
tour, _ = Tour.objects.get_or_create(slug='qa-gallery-fixture',defaults={'name':'QA gallery fixture — test images only',
    'summary':'An isolated test of the gallery. These artificial images do not represent Nova experiences.',
    'body':'UI test fixture only.','status':'PUBLISHED','legacy_publication':True})
option, _ = TourOption.objects.get_or_create(tour=tour,name='Test option', defaults={'duration_minutes':60,'mode':'PRIVATE','max_guests':7})
ExperienceRate.objects.get_or_create(experience=tour,option=option,name='Test rate',defaults={'amount':1,
    'duration_minutes':60,'max_guests':7,'effective_from':timezone.localdate()})
if not tour.images.exists():
    for index, color in enumerate(['#1b4066','#714478','#367455','#845727','#6c4460','#385b6b']):
        picture = Image.new('RGB',(1440,960),color)
        draw = ImageDraw.Draw(picture)
        draw.text((100,120),f'QA TEST IMAGE {index+1}',fill='white',font_size=80)
        stream = BytesIO(); picture.save(stream,'JPEG')
        ActivityImage.objects.create(tour=tour,image=SimpleUploadedFile(f'qa-{index+1}.jpg',stream.getvalue(),content_type='image/jpeg'),
            alt_text=f'Artificial QA test image {index+1}',caption=f'Test image {index+1} — not a product photo',
            is_primary=index==0,rights_confirmed=True,display_order=index)
print('Isolated UI fixture: http://127.0.0.1:8001/boat-rides/qa-gallery-fixture/',flush=True)
call_command('runserver','127.0.0.1:8001',use_reloader=False)
