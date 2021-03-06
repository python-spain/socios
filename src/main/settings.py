# -*- coding: utf-8 -*-

from os.path import join

from configurations import Configuration
from django.contrib.messages import constants as messages
from kaio import Options
from kaio.mixins import (CachesMixin, DatabasesMixin, CompressMixin, LogsMixin,
                         PathsMixin, SecurityMixin, DebugMixin, WhiteNoiseMixin)


opts = Options()


class Base(CachesMixin, DatabasesMixin, CompressMixin, PathsMixin, LogsMixin,
           SecurityMixin, DebugMixin, WhiteNoiseMixin, Configuration):
    """
    Project settings for development and production.
    """

    DEBUG = opts.get('DEBUG', True)

    BASE_DIR = opts.get('APP_ROOT', None)
    APP_SLUG = opts.get('APP_SLUG', 'socios')
    SITE_ID = 1
    SECRET_KEY = opts.get('SECRET_KEY', 'key')

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LANGUAGE_CODE = 'es'
    TIME_ZONE = 'Europe/Madrid'

    ROOT_URLCONF = 'main.urls'
    WSGI_APPLICATION = 'main.wsgi.application'

    INSTALLED_APPS = [
        # django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # apps
        'main',
        'libro',

        # 3rd parties
        'compressor',
        'constance',
        'cookielaw',
        'constance.backends.database',
        'django_extensions',
        'django_yubin',
        'kaio',
        'logentry_admin',
        'robots',
        'import_export',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # SecurityMiddleware options
    SECURE_BROWSER_XSS_FILTER = True

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert additional TEMPLATE_DIRS here
            ],
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.tz",
                    'django.template.context_processors.request',
                    'constance.context_processors.config',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]
            },
        },
    ]
    if not DEBUG:
        TEMPLATES[0]['OPTIONS']['loaders'] = [
            ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
        ]

    # Email
    EMAIL_BACKEND = 'django_yubin.smtp_queue.EmailBackend'
    DEFAULT_FROM_EMAIL = opts.get('DEFAULT_FROM_EMAIL', 'Example <info@example.com>')
    MAILER_LOCK_PATH = join(BASE_DIR, 'send_mail')

    # Bootstrap 3 alerts integration with Django messages
    MESSAGE_TAGS = {
        messages.ERROR: 'danger',
    }

    # Constance
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
    CONSTANCE_CONFIG = {
        'GOOGLE_ANALYTICS_TRACKING_CODE': ('UA-XXXXX-Y', 'Google Analytics tracking code.'),
    }


class Test(Base):
    """
    Project settings for testing.
    """

    def DATABASES(self):
        return self.get_databases(prefix='TEST_')
