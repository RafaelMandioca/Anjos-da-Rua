# anjosdaruaproject/settings/production.py
from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Make sure to set your actual domain name here
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# In production, we don't need the source SCSS files
# Django's `collectstatic` will handle the compiled CSS
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static'),
]