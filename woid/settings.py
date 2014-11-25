from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

from unipath import Path
import dj_database_url

PROJECT_DIR = Path(__file__).parent

SECRET_KEY = 'kf(-@ucujwc*ce%*-(w8$-%&ihmj)90^5w9tc*(-y!fxoaib%g'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'woid.activities',
    'woid.core',
    'woid.feed',
    'woid.notifications',
    'woid.questions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'woid.urls'

WSGI_APPLICATION = 'woid.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
      default = 'postgres://u_woid:123@localhost:5432/woid')
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

MEDIA_ROOT = PROJECT_DIR.parent.child('media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

NO_PICTURE = ''

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)
