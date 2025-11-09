# phase1/settings/__init__.py
"""
Expose a default settings module when DJANGO_SETTINGS_MODULE is not set.
When running manage.py locally you can set DJANGO_SETTINGS_MODULE or
export DJANGO_ENV to choose between 'development' or 'production'.
"""
import os

# Either set DJANGO_SETTINGS_MODULE externally (preferred),
# or fall back to a sensible default.
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if DJANGO_SETTINGS_MODULE:
    # If DJANGO_SETTINGS_MODULE is set use Django's usual mechanism by leaving it alone.
    # This file only exists so package imports succeed.
    pass
else:
    # fallback: use DJANGO_ENV var to decide
    env = os.environ.get('DJANGO_ENV', 'development').lower()
    if env == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phase1.settings.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phase1.settings.development')
