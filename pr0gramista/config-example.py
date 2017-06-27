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

debug = True

# If debug is False this list must be filled
ALLOWED_HOSTS = []

MEDIA_ROOT = ''

ANALYTICS = 'UA-XXXXX'
