from .base import *


SECRET_KEY = "django-insecure-938!cr))pzsc2-9#!=+u17v(-lkb5i+qr49vij7bw*1%dujb@s"

DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
