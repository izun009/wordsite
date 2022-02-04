from .base import *

DEBUG = True

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Database Development
DATABASES = {
    'default': env.db_url(
        'SQLITE_URL'
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'renditions': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
        'TIMEOUT': 600,
    }
}

try:
    from .local import *
except ImportError:
    pass
