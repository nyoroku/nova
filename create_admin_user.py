import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boats.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'novaboats')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@novaboatrider.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'naivasha101010??')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"[OK] Superuser '{username}' created successfully.")
else:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"[OK] Superuser '{username}' password updated successfully.")
