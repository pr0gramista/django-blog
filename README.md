# Blog engine for [pr0gramista.pl](https://pr0gramista.pl) [![Build Status](https://travis-ci.org/pr0gramista/pr0gramista.svg?branch=master)](https://travis-ci.org/pr0gramista/pr0gramista) [![codecov](https://codecov.io/gh/pr0gramista/pr0gramista/branch/master/graph/badge.svg)](https://codecov.io/gh/pr0gramista/pr0gramista)

Written in Python, powered by django.

### Easy config

Separate config file for easy and secure (git-proof) deployment.

### Plugins/django apps

- django-taggit - simple tagging system
- django-imagekit - image processing library, used for all graphics hosted on blog
- mistune - Markdone compiler, extended for awesome features

#### Clean

The code is free of magic, except django.

#### RSS

Blog generates RSS feeds, yay!

#### Tests

There are tests, not many of them, but they make critical things intact (like not seeing unpublished posts).

**It also has an interesting 404 page.**

### Contributing

Just don't put `npm` here and I will be happy.

### Development

```
pip install -r requirements.txt
cp pr0gramista/config-example.py pr0gramista/config.py
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Deployment

Copy `config-example.py` to `config.py` and set your secret key, `debug = False`, allowed hosts and `STATIC_ROOT` and `MEDIA_ROOT`. You can use almost any database, but SQLite and MySQL will work out of the box. You will propably need a WSGI Server like [Gunicorn](http://gunicorn.org/) and HTTP Server like [nginx](https://nginx.org/). Have fun!
