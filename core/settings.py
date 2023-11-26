from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qfr9p_+x+c#i9)tmy1z)5i@_ofwwflzfy)llogwzuw&lv=@!2!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # Custom Apps
    # 'daphne',
    'channels',
    'api',

    # app
    'django.contrib.sites',  # must
    'allauth',  # must
    'allauth.account',  # must
    'allauth.socialaccount',  # must
    'allauth.socialaccount.providers.google',  # new
    'crispy_forms',
    'razorpay',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # custom headers
    'api.middleware.CustomErrorHandlerMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


#sqlite database

 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# from urllib.parse import quote_plus
# #mongodb database
# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'finalweb',
#         'CLIENT': {
#             'host': 'mongodb+srv://evc:' + quote_plus('@M0hammed@') + '@cluster0.qmgookq.mongodb.net/?retryWrites=true&w=majority',
#             'username': 'evc',
#             'password': '@M0hammed@',
#         },
#     }
# }






# mysql database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'webapp',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

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

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# app

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    'social_core.backends.google.GoogleOAuth2',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


ACCOUNT_EMAIL_VERIFICATION = 'none'

LOGIN_REDIRECT_URL = '/'


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '549980185966-7mgi7dm4blun8t0jpc1mp2gtj2skp4qp.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


# django-phonenumber-field settings
PHONENUMBER_DB_FORMAT = 'NATIONAL'


RAZORPAY_KEY_ID = "rzp_test_Hq5PGGGXL04xp4"
RAZORPAY_KEY_SECRET = "ctgyxd6pdR6UQODnuJ1W9p30"


# RAZORPAY_KEY_ID ='rzp_live_XSRZsaKtueOJbw'
# RAZORPAY_KEY_SECRET ='f0HQ5Yh8oSOqyrvwyCApA6T8'


SMS_GATEWAY_API_KEY = '3425207861743338098'
# SMS_GATEWAY_SECRET_KEY = '3425207861743338098'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')




#dashboard
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
