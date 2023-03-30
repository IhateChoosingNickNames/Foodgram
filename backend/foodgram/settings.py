import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    default="django-insecure-e877=zax0li(2+kbp(ocp2@=6agden5&)t60up-=9c8srd8ndf",
)

DEBUG = True

ALLOWED_HOSTS = (
    "localhost",
    "backend",
    "127.0.0.1",
    "foodgram.myftp.org",
    "158.160.11.231",
    "0.0.0.0",
)


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "api.apps.ApiConfig",
    "recipes.apps.RecipesConfig",
    "users.apps.UsersConfig",
    "core.apps.CoreConfig",

    "rest_framework.authtoken",
    "rest_framework",
    "djoser",
    "django_filters",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

CSRF_TRUSTED_ORIGINS = ("http://127.0.0.1", "https://foodgram.myftp.org")

ROOT_URLCONF = "foodgram.urls"

TEMPLATE_DIR = BASE_DIR.parent / "docs"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (TEMPLATE_DIR,),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
)

WSGI_APPLICATION = "foodgram.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default="django.db.backends.postgresql"),
        'NAME': os.getenv('DB_NAME', default="postgres"),
        'USER': os.getenv('POSTGRES_USER', default="postgres"),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default="adm"),
        'HOST': os.getenv('DB_HOST', default="db"),
        'PORT': os.getenv('DB_PORT', default="5432")
    }
}

AUTH_PASSWORD_VALIDATORS = (
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
)

INTERNAL_IPS = ("127.0.0.1",)

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = "backend_static/"
STATIC_ROOT = BASE_DIR / "backend_static"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": "10000/day",
        "anon": "1000/day",
    },
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}


DJOSER = {
    "SERIALIZERS": {
        "user": "users.serializers.CustomUserSerializer",
        "current_user": "users.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
        "user_list": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",)
    },
}
