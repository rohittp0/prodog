import os
# from glob import glob
from pathlib import Path
import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_KEY")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
HOST = os.getenv("HOST", "localhost")

IN_DOCKER = os.getenv("IN_DOCKER", "false").lower() == "true"

# uncomment to use GDAL and GEOS in postgis
# if IN_DOCKER:
#     GDAL_LIBRARY_PATH = glob("/usr/lib/libgdal.so.*")[0]
#     GEOS_LIBRARY_PATH = glob("/usr/lib/libgeos_c.so.*")[0]
# else:
#     GDAL_LIBRARY_PATH = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
#     GEOS_LIBRARY_PATH = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"

REDIS_HOST = "redis" if IN_DOCKER else "localhost"
REDIS_URL = f"redis://{REDIS_HOST}:6379/1"

LOG_BASE_URL = os.getenv("LOG_BASE_URL")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",") + [HOST, "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://{HOST}", "https://{HOST}"]

CORS_ALLOW_ALL_ORIGINS = True  # TODO Change to required domains only

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SAMESITE = None  # or 'None'
SESSION_COOKIE_SECURE = True  # if using HTTPS
CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = True

VERTICAL="hotel"

# Application definition
INSTALLED_APPS = [
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    # "rest_framework_gis",
    # "django.contrib.gis",
    "django.contrib.postgres",
    "django_filters",
    "rest_framework",
    "drf_yasg",
    "corsheaders",
    "home.apps.HomeConfig"

    # Local apps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql", # "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.paginator.DefaultResultsSetPagination",
    "PAGE_SIZE": 30,
}

# Redis Configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 100,
        },
    }
}

INTERNAL_IPS = ["127.0.0.1"]

AUTH_PASSWORD_VALIDATORS = []

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # The handler’s level can be DEBUG (to handle all levels passed to it)
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        # Root logger: only show WARNING and above
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # django.request logger: show ALL levels (DEBUG or higher)
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
