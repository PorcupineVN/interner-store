"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6#$jd1$kqba+z6^!v5u&*tqmvae=w1g&7rm)-$vhkd^%-e0es2'
DJANGO_PRODUCTION = bool(os.environ.get('DJANGO_PRODUCTION', False))
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = not DJANGO_PRODUCTION

ALLOWED_HOSTS = ['127.0.0.1'] if DJANGO_PRODUCTION else []
INTERNAL_IPS = ["127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'template_profiler_panel',
    'social_django',
    'django_extensions',
    'pydotplus',

    'mainapp',
    'authapp',
    'basketapp',
    'adminapp',
    'ordersapp',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',

]

ROOT_URLCONF = 'geekshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.basket',
                'mainapp.context_processors.menu_links',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'geekshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if DJANGO_PRODUCTION:
    DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', 'django')
    DJANGO_DB_USER = os.environ.get('DJANGO_DB_USER', 'django')
    DJANGO_DB_PASSWORD = os.environ.get('DJANGO_DB_PASSWORD', 'django')
    DJANGO_DB_HOST = os.environ.get('DJANGO_DB_HOST', '127.0.0.1')
    DJANGO_DB_PORT = int(os.environ.get('DJANGO_DB_PORT', '5432'))

    assert all(
        DJANGO_DB_NAME,
        DJANGO_DB_USER,
        DJANGO_DB_PASSWORD,
        DJANGO_DB_HOST,
        DJANGO_DB_PORT,
    )
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DJANGO_DB_NAME,
            'USER': DJANGO_DB_USER,
            'PASSWORD': DJANGO_DB_PASSWORD,
            'HOST': DJANGO_DB_HOST,
            'PORT': DJANGO_DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#Auth
AUTH_USER_MODEL = "authapp.ShopUser"

LOGIN_URL = 'auth:login'

DOMAIN_NAME = 'http://localhost:8000'

EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'django@geekshop.local'
EMAIL_HOST_PASSWORD = 'geekshop'
EMAIL_USE_SSL = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
)

with open('geekshop/vk.json', 'r') as f:
    VK = json.load(f)
    SOCIAL_AUTH_VK_OAUTH2_KEY = VK['SOCIAL_AUTH_VK_OAUTH2_KEY']
    SOCIAL_AUTH_VK_OAUTH2_SECRET = VK['SOCIAL_AUTH_VK_OAUTH2_SECRET']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'authapp.pipeline.save_user_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

DEBUG_TOOLBAR_PANELS = [
'debug_toolbar.panels.versions.VersionsPanel',
'debug_toolbar.panels.timer.TimerPanel',
'debug_toolbar.panels.settings.SettingsPanel',
'debug_toolbar.panels.headers.HeadersPanel',
'debug_toolbar.panels.request.RequestPanel',
'debug_toolbar.panels.sql.SQLPanel',
'debug_toolbar.panels.templates.TemplatesPanel',
'debug_toolbar.panels.staticfiles.StaticFilesPanel',
'debug_toolbar.panels.cache.CachePanel',
'debug_toolbar.panels.signals.SignalsPanel',
'debug_toolbar.panels.logging.LoggingPanel',
'debug_toolbar.panels.redirects.RedirectsPanel',
'debug_toolbar.panels.profiling.ProfilingPanel',
'template_profiler_panel.panels.template.TemplateProfilerPanel',
'template_profiler_panel.panels.template.TemplateProfilerPanel',
]

def show_toolbar(request):
    return bool(request.GET.get('debug'))

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}