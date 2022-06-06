import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


env = environ.Env()
environ.Env.read_env()

STATIC_URL = 'static/'  # uncomment in development


# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_ROOT = 'static_root'
# # Change aws links
# # User Access
# AWS_ACCESS_KEY_ID = 'AKIAQGTQMVL3ZUYQW35Y'
# AWS_SECRET_ACCESS_KEY = '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'

# # Aws settings
# AWS_STORAGE_BUCKET_NAME = 'venture-cars-1'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# designate ecommerce/static/images to where
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
