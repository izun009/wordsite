from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['yourdomain.com']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379/1",
            "redis://127.0.0.1:6379/2",
            "redis://127.0.0.1:6378/1",
        ],
        "OPTIONS": {
            'PASSWORD': 'PLEASE SETUP YOUR REDIS PASSWORD', # Setup your redis password for security
            "CLIENT_CLASS": "django_redis.client.ShardClient",
        }
    },
    # for image rendition
    'renditions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6377/1',
        'OPTIONS': {
            'PASSWORD': 'PLEASE SETUP YOUR REDIS PASSWORD', # Setup your redis password for security
            "CLIENT_CLASS": "django_redis.client.ShardClient",
        },
        'TIMEOUT': 600,
    }
}

try:
    from .local import *
except ImportError:
    pass
