# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
from django.conf import settings
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# import settings debug will be false always since file is not ready so extrat direct from .env
# settings.DEBUG
DEBUG = config("DEBUG", default=False, cast=bool)

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
            "OPTIONS": {
                # Enable MySQL strict mode. "MySQL's Strict Mode fixes many data
                # integrity problems in MySQL, such as data truncation upon
                # insertion, by escalating warnings into errors."
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
