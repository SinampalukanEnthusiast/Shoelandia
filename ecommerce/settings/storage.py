import os
import environ
from pathlib import Path
from storages.backends.s3boto3 import S3Boto3Storage
BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env()
environ.Env.read_env()

# STATIC_URL = '/static/'
# STATIC_ROOT = 'static_root'


class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# User Access
AWS_ACCESS_KEY_ID = 'AKIAQGTQMVL3ZUYQW35Y'
AWS_SECRET_ACCESS_KEY = '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'

# Aws settings
AWS_STORAGE_BUCKET_NAME = 'shoelandia'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
DEFAULT_FILE_STORAGE = 'ecommerce.settings.storage.MediaStore'
# designate ecommerce/static/images to where
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
