import os

# SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

# MySQL
#db = {
#    'ENGINE': 'django.db.backends.mysql',
#    'HOST': db_host,
#    'NAME': db_name,
#    'USER': db_user,
#    'PASSWORD': db_password,
#}

# Change this!
secret = r'=0fcb5b%3wiqj6v&@yc(8lg8mwh5k#vb^ib1brux+em$t$q8_t'

# Definitely change this in production
debug = True

# If debug is False this list must be filled
ALLOWED_HOSTS = []

# You should probably change those to something like /var/www/static etc.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Put your Google Analytics tag here
ANALYTICS = 'UA-XXXXX'
