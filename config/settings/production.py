
import dj_database_url
import os

from config.settings.common import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['newsaggregatoralpha.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}
