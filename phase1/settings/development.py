from .base import *

# Development-specific
DEBUG = True

# Allow localhost and any local IP
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# Use PostgreSQL as the local DB unless DATABASE_URL is provided
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        "default": dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "SPARK_db",        
            "USER": "postgres",        
            "PASSWORD": "05172003", 
            "HOST": "localhost",            
            "PORT": "5432",                 
        }
    }

# Useful dev settings
INTERNAL_IPS = ["127.0.0.1"]

# Development static files — serve with Django's staticfile finder (no whitenoise storage)
STATICFILES_DIRS = getattr(globals(), 'STATICFILES_DIRS', [])  # inherited from base
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_dev')

# Local email backend for testing
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"