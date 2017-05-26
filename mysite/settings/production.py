#import os
from mysite.settings.base_settings import *

SECRET_KEY = '=mr&_u3u6wtdfq)=6)&jn!gq3wd-q6)cl$(#chfrwo4bz^wzb1'
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']
#ALLOWED_HOSTS = ['104.131.184.18', 'www.kudzu.cc', 'kudzu.cc']

# Application definition

INSTALLED_APPS = [
	'nltk',
	'PyPDF2',
	'datetimewidget', #https://github.com/asaglimbeni/django-datetime-widget
	'ats.apps.AtsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

SECURE_HSTS_SECONDS = 20 ##change for production?
#https://docs.djangoproject.com/en/1.11/ref/middleware/#http-strict-transport-security
#https://hstspreload.org/
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
