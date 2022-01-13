import os

from config.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY'] 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

