# # phase1/settings/production.py
# from .base import *
# import dj_database_url

# DEBUG = False

# # Production ALLOWED_HOSTS must be set via env var or Render provides RENDER_EXTERNAL_HOSTNAME
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['two025-cp-section-placement-and-student.onrender.com'])
# render_host = env('RENDER_EXTERNAL_HOSTNAME', default=None)
# if render_host:
#     ALLOWED_HOSTS.append(render_host)

# # Secure proxy header (Render / proxy)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # Database — require DATABASE_URL in production
# DATABASES = {
#     "default": dj_database_url.parse(env('DATABASE_URL'))
# }
# # Keep persistent connections
# DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=600)

# # Security hardening
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
# SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=3600)  # tune for your release
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)
# SECURE_CONTENT_TYPE_NOSNIFF = True

# # Static files: enable whitenoise compressed manifest storage
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # Logging (simple example)
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': { 'class': 'logging.StreamHandler' },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
# }

# phase1/settings/production.py
from .base import *
import dj_database_url

# -----------------------------------------------------
# ✅ PRODUCTION SETTINGS
# -----------------------------------------------------
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent.parent, '.env'))
DEBUG = False

# --- Hosts ---
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])
RENDER_EXTERNAL_HOSTNAME = env('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- Database ---
DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=600)

# --- Security ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# --- Static & Media ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Logging ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

print("🚀 Using PRODUCTION settings")
