from decouple import config

from .base import *


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=True, cast=bool)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
