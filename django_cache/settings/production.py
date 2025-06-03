from .base import *
from .cache import *
import os
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Generate a new secret key for production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-production-key-change-this-in-environment-variable')

# Allow specific hosts or domains
ALLOWED_HOSTS = ['*']  # Replace with your domain or EC2 IP in production

# Database settings for MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'django_db'),
        'USER': os.environ.get('DB_USER', 'django_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_secure_password'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Redis settings for cacheops
# Override the Redis URL for production
CACHEOPS_REDIS = os.environ.get('CACHEOPS_REDIS', 'redis://redis:6379/1')

# Enable caching in production
ENABLE_CACHEOPS = os.environ.get('ENABLE_CACHEOPS', 'TRUE') == 'TRUE'

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'

# Security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (enable when you have SSL set up)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# HSTS settings (enable when you have SSL set up)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
