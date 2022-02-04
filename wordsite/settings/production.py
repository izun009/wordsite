from .base import *

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['yourdomain.com']

# Database Production
DATABASES = {
    'default': env.db_url(
        'SQLITE_URL'
    ),
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379/1",
            "redis://127.0.0.1:6379/2",
        ],
        "OPTIONS": {
            # 'PASSWORD': 'PLEASE SETUP YOUR REDIS PASSWORD', # Setup your redis password for security
            "CLIENT_CLASS": "django_redis.client.ShardClient",
        }
    },
}

try:
    from .local import *
except ImportError:
    pass
