from . import *
import os
import raven
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/staticfiles/'

# Static files settings	
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))	

STATIC_ROOT = os.path.join(PROJECT_ROOT, './staticfiles')	

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (	
    os.path.join(PROJECT_ROOT, 'staticfiles'),	
)