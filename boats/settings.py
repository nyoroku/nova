# boats/settings.py
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='nova-electric-2026-production-secret-key-lake-naivasha')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://novaboats.pythonanywhere.com',
    'https://novaboatrider.com',
    'https://www.novaboatrider.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'taggit',
    "tinymce",

    # Nova Production Architecture
    'core.apps.CoreConfig',
    'tours.apps.ToursConfig',
    'partners.apps.PartnersConfig',
    'stays.apps.StaysConfig',
    'packages.apps.PackagesConfig',
    'bookings.apps.BookingsConfig',
    'content.apps.ContentConfig',
    'seo.apps.SeoConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seo.middleware.RedirectMiddleware',
]

# Security/Performance Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'boats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.nova_site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'boats.wsgi.application'

TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "100%",
    "menubar": False,
    "plugins": [
        "advlist autolink lists link image preview anchor",
        "searchreplace visualblocks code fullscreen",
        "media table paste code help wordcount"
    ],
    "toolbar": (
        "undo redo | formatselect | bold italic | bullist numlist | link image | removeformat | code"
    ),
    "block_formats": "Paragraph=p;Heading 2=h2;Heading 3=h3;Heading 4=h4",
    "paste_as_text": True,
    "paste_remove_spans": True,
    "paste_remove_styles": True,
    "valid_elements": "p,h2,h3,h4,strong/b,em/i,ul,ol,li,a[href|title],img[src|alt|width|height]",
    "invalid_elements": "font,span,style",
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Kiswahili'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('zh-hans', '中文 (简体)'),
    ('ar', 'العربية'),
    ('hi', 'हिन्दी'),
    ('nl', 'Nederlands'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WHITENOISE_MAX_AGE = 31536000
WHITENOISE_INDEX_PAGE_SELF_REDIRECTION = True
WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Nova Brand Constants (Single source of truth)
SITE_NAME = "Nova Boat Rides Naivasha"
SITE_SHORT_NAME = "Nova"
SITE_DOMAIN = "novaboatrider.com"
SITE_URL = f"https://www.{SITE_DOMAIN}"
SITE_PHONE_DISPLAY = "+254 701 215 295"
SITE_PHONE_E164 = "+254701215295"
SITE_WHATSAPP_NUMBER = "254701215295"
SITE_EMAIL = "hello@novaboatrider.com"
ADMIN_TITLE = "Nova Boat Rides Admin"
ADMIN_HEADER = "Nova Boat Rides"
ADMIN_INDEX_TITLE = "Nova Operations Portal"
ADMIN_NAME = "Nova Boat Rides"
