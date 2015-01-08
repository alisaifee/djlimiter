"""
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'hrzeqwz0@nps2#ns3_qkqz*#5=)1bxcdwa*h__hta0f1bqr2e!'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

TEMPLATE_DIRS = ("tests/templates", )

INSTALLED_APPS = (
    'django_nose',
)
for dir in os.listdir("tests/apps"):
    if os.path.isdir("tests/apps/%s" % dir):
        INSTALLED_APPS += ( "tests.apps.%s" % dir, )


MIDDLEWARE_CLASSES = (
)

ROOT_URLCONF = 'tests.urls'

WSGI_APPLICATION = 'tests.wsgi.application'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


