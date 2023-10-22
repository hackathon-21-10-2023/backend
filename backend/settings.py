from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv("DJANGO_SECRET_KEY", "django-insecure-hackme)v-k30zzqj&%3!&=g8iz+szz^1hj$%!u4#0jf=0ob1o=")

DEBUG = getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = getenv("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1]").split()

CSRF_TRUSTED_ORIGINS = getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "http://127.0.0.1:8023").split()


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'drf_yasg',
    "api.apps.ApiConfig",
    'chat_gpt.apps.ChatGptConfig',
    'auth_token.apps.AuthTokenConfig',
    'rest_framework'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"]
        ,
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

WSGI_APPLICATION = "backend.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": getenv("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": getenv("SQL_USER", "user"),
        "PASSWORD": getenv("SQL_PASSWORD", "hackme"),
        "HOST": getenv("SQL_HOST", "localhost"),
        "PORT": getenv("SQL_PORT", "5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_token.authentication.JWTAuthentication',
        )
}

AUTH_USER_MODEL = 'api.User'


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

BASE_URL_SWAGGER = getenv("BASE_URL_SWAGGER", "http://127.0.0.1:8000")
