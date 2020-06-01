"""Base settings file; used by manage.py. All settings can be overridden via
local_settings.py"""
import os
import dj_database_url
from django.utils.crypto import get_random_string

ALLOWED_HOSTS = [
    value for key, value in os.environ.items()
    if key.startswith('ALLOWED_HOST')
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'mptt',
#    'haystack',
    'regcore',
    'regcore_read',
    'regcore_write',
]
MIDDLEWARE_CLASSES = []

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_string(50))


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'eregs.db'
#    }
#}

DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]

ROOT_URLCONF = 'regcore.urls'

DEBUG = True

# Configurable storage backends, keyed by data_type (e.g. regulations, diffs)
# If a key is not set, defaults to regcore.db.django_models versions
BACKENDS = {}

#ELASTIC_SEARCH_URLS = []
#ELASTIC_SEARCH_INDEX = 'eregs'

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#    }
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        }
    }
}

#SEARCH_HANDLER = 'regcore_read.views.haystack_search.search'
BACKENDS = {
    'regulations': 'regcore.db.django_models.DMRegulations',
    'layers': 'regcore.db.django_models.DMLayers',
    'notices': 'regcore.db.django_models.DMNotices',
    'diffs': 'regcore.db.django_models.DMDiffs'
}

INSTALLED_APPS.append('regcore_pgsql')
SEARCH_HANDLER = 'regcore_pgsql.views.search'

# Batch size used in `bulk_create`; defaults to a conservative value to avoid
# hitting SQLite limits
BATCH_SIZE = 50

# Lower bound for search results to appear when using pgsql search
PG_SEARCH_RANK_CUTOFF = 0.15

_envvars = ('HTTP_AUTH_USER', 'HTTP_AUTH_PASSWORD')
for var in _envvars:
    globals()[var] = os.environ.get(var)

try:
    from local_settings import *
except ImportError:
    pass
