"""
Django settings for mysite project (Render + local dev).
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-development-key")

# Default to DEBUG=False unless explicitly set
DEBUG = os.environ.get("DEBUG", "False") == "True"


ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "harrisonogdencarr.pythonanywhere.com",
]

# Render injects its hostname into env
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "projects.apps.ProjectsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files in prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "projects.context_processors.portfolio_years",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
if os.environ.get("DATABASE_URL"):
    # Render Postgres
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Include both the top-level static/ folder and any app-level static/ folders
STATICFILES_DIRS = [
    BASE_DIR / "projects" / "static",
]


if DEBUG:
    # Simple storage in dev (no hashed filenames)
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    # WhiteNoise compressed storage in prod
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------------------------------------------------------------
# Media files (still available if you need uploads, but not for fixed screenshots)
# -----------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------------------------------------------------------
# Default primary key field type
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"