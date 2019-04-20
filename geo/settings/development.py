from .base import *
from .config import *


DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'yf&eh^bz(imf(7kal9iqo*+*tmw67muq*g&%djdzwlp2$ysg+p'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geodb',
        'USER': 'geo',
        'PASSWORD': 'Ge0dB',
        'HOST': 'localhost',
        'PORT': '',
    }
}
