import os
import sys

import django
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework.authtoken',
            'drf_spectacular',
            'api',
        ],
        SECRET_KEY='test-secret-key-for-pytest',
        USE_TZ=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        REST_FRAMEWORK={
            'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        },
    )

django.setup()
