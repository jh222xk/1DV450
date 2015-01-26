"""
Django settings for toerh project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Throw error if we haven't set the TOERH_DJANGO_SECRET_KEY in the environment
assert 'TOERH_DJANGO_SECRET_KEY' in os.environ, 'Set TOERH_DJANGO_SECRET_KEY in your environment!'
SECRET_KEY = os.environ['TOERH_DJANGO_SECRET_KEY']

# Debug
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('rest_framework.authentication.OAuth2Authentication',
         'rest_framework.authentication.SessionAuthentication'),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES':
        ('rest_framework.permissions.IsAuthenticated',)
}


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'provider',
    'provider.oauth2',

    # Own apps
    'positioningservice',
)

# Middleware classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'toerh.urls'

WSGI_APPLICATION = 'toerh.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '../static')

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}