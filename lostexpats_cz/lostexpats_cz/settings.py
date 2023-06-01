"""
Django settings for lostexpats_cz project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from django import apps
from pathlib import Path
import os 
import logging.handlers
import logging 
from django.http import HttpResponse 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_HOST = 'host_patterns'
ROOT_HOSTCONF = 'lostexpats_cz.hosts'

SECURE_HSTS_SECONDS = 31536000 #1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SECURE_SSL_REDIRECT = True
# Redirects all HTTP requests to HTTPS for secure communication

SSL_ENABLED = True
# Indicates that SSL (Secure Sockets Layer) is enabled

SSL_CERTIFICATE = '/path/to/cert.pem'
# Specifies the path to the SSL certificate file

SSL_KEY = '/path/to/key.pem'
# Specifies the path to the SSL key file

SESSION_COOKIE_SECURE = True
# Ensures that the session cookie is only sent over HTTPS

CSRF_COOKIE_SECURE = True
# Ensures that the CSRF (Cross-Site Request Forgery) cookie is only sent over HTTPS

# session data will be stored in the database.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_AGE = 86400  # 24 hours

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'authentication.apps.AuthenticationConfig',
    'django.contrib.staticfiles',
    'sslserver',
    'django_hosts',

]

MIDDLEWARE = [
    # Enforces security measures in the Django application
    'django.middleware.security.SecurityMiddleware',
    # Enables support for Django sessions
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Provides common HTTP request and response operations
    'django.middleware.common.CommonMiddleware',
    # Adds protection against Cross-Site Request Forgery (CSRF) attacks
    'django.middleware.csrf.CsrfViewMiddleware',
    # Handles user authentication and sets the 'user' attribute in the request
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Handles messages (e.g., success messages, error messages) between requests
    'django.contrib.messages.middleware.MessageMiddleware',
    # Protects against clickjacking attacks by setting the X-Frame-Options header
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Safeguards user privacy
    'lostexpats_cz.referrer_middleware.ReferrerPolicyMiddleware',
]


#When protecting the webiste from click-jacking there are 
#three settings to choose from which include 'same-origin', 'deny', and 'ALLOW-FROM origin'(the last option does not work on most 
# browsers now). For our application we chose to 'deny' because it denies all options of framing which gives the least risk for clickjacking too. 
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
 #The page cannot be displayed in a frame, regardless of the site attempting to do so.

ROOT_URLCONF = 'lostexpats_cz.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        # Specifies the directories where Django looks for template files
        'APP_DIRS': True,
        # Determines whether Django looks for template files in installed apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # Adds the debug context processor for template debugging
                'django.template.context_processors.request',
                # Adds the request context processor for accessing request data in templates
                'django.contrib.auth.context_processors.auth',
                # Adds the auth context processor for including authentication-related data in templates
                'django.contrib.messages.context_processors.messages',
                # Adds the messages context processor for including messages framework data in templates
                'authentication.context_processors.cookie_banner',
                # Adds a custom context processor 'cookie_banner' from the 'authentication' app
            ],
        },
    },
]


WSGI_APPLICATION = 'lostexpats_cz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# settings.py

# ...

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# settings.py

# ...

STATICFILES_DIRS = [
    '/lostexpats_cz/static',
    ]

# ...


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ...

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


# Configure the Django CSP settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "fonts.googleapis.com", "cdn.jsdelivr.net")
CSP_SCRIPT_SRC = ("'self'", "cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com", "cdn.jsdelivr.net")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'self'",)

# CONFIGURE APP EMAIL BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP server's hostname or IP address
EMAIL_PORT = 587  # Replace with the appropriate port number
EMAIL_HOST_USER = 'lostexpatscz@gmail.com'  # Replace with your SMTP server's username
EMAIL_HOST_PASSWORD = 'rnsbqsvowbnvkdro'  # Replace with your SMTP server's password
EMAIL_USE_TLS = True  # Set to True if your SMTP server requires a TLS connection
DEFAULT_FROM_EMAIL = 'lostexpatscz@gmail.com' 


# settings.py
# Ensure the logs directory exists
os.makedirs(os.path.dirname('logs/user_login.log'), exist_ok=True)

# Define a function to set a cookie in the HTTP response
def set_cookie(request):
    # Create a new HttpResponse object
    response = HttpResponse()
    # Set a cookie named 'cookie_name' with the value 'cookie_value'
    response.set_cookie('cookie_name', value='cookie_value')
    # Return the HttpResponse object with the cookie set
    return response

# Configure the logging settings
LOGGING = {
    # This key specifies the version of the logging configuration.
    'version': 1,
    # This key determines whether existing loggers should be disabled 
    # when the configuration is applied.
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/user_login.log',
            'formatter': 'standard',
        },
    },
    #  This key is a dictionary of log formatters. 
    # In this case, there is only one formatter defined, named 'standard'.
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    #  'file' handler should be used and sets the log level to 'INFO'.
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}


# ...
