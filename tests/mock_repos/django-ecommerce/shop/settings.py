# shop/settings.py - Django E-Commerce Settings (INTENTIONALLY FLAWED FOR AUDIT TESTING)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure-sk+!3x@q5z9&8w^1e4r7t0y^u3i6o9p'  # FLAW: Hardcoded secret key
STRIPE_API_KEY = 'FAKE_STRIPE_TEST_KEY_FOR_AUDIT_DEMO_ONLY'  # FLAW: Hardcoded Stripe test key
DEBUG = True  # FLAW: DEBUG=True should not be in production

ALLOWED_HOSTS = ['*']  # FLAW: Wildcard allowed hosts

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'orders',
    'products',
    'payments',
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopdb',
        'USER': 'INTENTIONALLY_FAKE_DB_USER_FOR_AUDIT_TEST',
        'PASSWORD': 'INTENTIONALLY_FAKE_DB_PASSWORD_FOR_AUDIT_TEST',  # FLAW: Hardcoded DB password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # FLAW: Default AllowAny permission
    ],
}

# Missing: SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE
# Missing: SECURITY_HEADERS
