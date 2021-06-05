from decouple import config

from .base import *


SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [config("HOST_URL")]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS
CORS_ALLOWED_ORIGINS = config(
    "FRONTEND_URLS", cast=lambda urls: [url.strip() for url in urls.split(",")]
)
