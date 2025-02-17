from . import justfix_environment  # noqa

justfix_environment.IS_RUNNING_TESTS = True

from .settings import *  # noqa

# Disable 2FA by default.
TWOFACTOR_VERIFY_DURATION = 0

# Disable legacy auth by default, tests will need
# to override settings if they want to enable it.
LEGACY_MONGODB_URL = ''

# Disable Twilio by default.
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''

# Disable a bunch of third-party integrations by default.
GEOCODING_SEARCH_URL = ""
AIRTABLE_API_KEY = ''
SLACK_WEBHOOK_URL = ''
GA_TRACKING_ID = ''
FACEBOOK_PIXEL_ID = ''
ROLLBAR_ACCESS_TOKEN = ''
MAPBOX_ACCESS_TOKEN = ''
NYCDB_DATABASE = None
ROLLBAR = {}  # type: ignore
LOGGING['handlers']['rollbar'] = {  # type: ignore  # noqa
    'class': 'logging.NullHandler'
}
HP_ACTION_CUSTOMER_KEY = ''
RAPIDPRO_API_TOKEN = ''
LOB_SECRET_API_KEY = ''
LOB_PUBLISHABLE_API_KEY = ''

DEBUG_DATA_DIR = ''

DEFAULT_FILE_STORAGE = 'project.settings_pytest.NotActuallyFileStorage'

# Use defaults for static file storage.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_URL = '/static/'

# Use very fast but horribly insecure password hashing
# to make tests run faster.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Access to the nycdb is read-only anyways, so we won't be able to create a
# test database on it.
if 'nycdb' in DATABASES:  # noqa
    del DATABASES['nycdb']  # noqa


class NotActuallyFileStorage:
    def __init__(self):
        raise Exception(
            'Please use the django_file_storage pytest fixture if '
            'you need to use Django file storage'
        )
