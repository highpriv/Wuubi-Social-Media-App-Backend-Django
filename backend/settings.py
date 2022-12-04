import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATE_INPUT_FORMATS = ['%d-%m-%Y']

SITE_ID = 1

SECRET_KEY = '_g#b8gr92b+1qtg28r7p!94%)y$b-9)-4k$2di=vhc_1sk=-dp'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = 30242880

ASGI_APPLICATION = 'backend.asgi.application'

INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'tinymce',
    'django_crontab',
    'django_rest_passwordreset',
]


POINTS_SETTINGS={
    "CREATE_ARTICLE":200,
    "CREATE_COMMENT": 10,
    "CREATE_GROUP": 100,
    "GROUP_CONTENT": 10,
    "GROUP_COMMENT": 2
}



JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'backend.utils.my_jwt_response_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}



CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8081",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://localhost:8081",
    "http://localhost:8081/post/",
    "http://localhost:8081/post/*",
    "http://localhost:8081/post/*/",
    "http://127.0.0.1:8081/post/",
    "http://127.0.0.1:8081/post/*",
    "http://127.0.0.1:8081/post/*/"
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'http://localhost:8081',
    'localhost:8081',
    '127.0.0.1:8081',
    '127.0.0.1:4200',
    'http://localhost:4200',
    "http://localhost:8081/post/",
    "http://localhost:8081/post/*",
    "http://localhost:8081/post/*/",
    "http://127.0.0.1:8081/post/",
    "http://127.0.0.1:8081/post/*",
    "http://127.0.0.1:8081/post/*/"
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOGIN_URL = "/account/login/"

#gmail_send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'highpriv@gmail.com'
EMAIL_HOST_PASSWORD = 'wybyekmcligyxloh' #past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'


POSTMAN_AUTO_MODERATE_AS = True

WSGI_APPLICATION = 'backend.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = {
#        'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'wuubi',
#        'USER' : 'canberk2',
#        'PASSWORD' : '12323345Ab.',
#        'HOST' : 'localhost',
#        'PORT' : '5432',
#        }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')

