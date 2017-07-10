# Blog engine for [pr0gramista.pl](https://pr0gramista.pl)
Written in Python, powered by django.

### Easy config
Separate config file for easy and secure (git-proof) deployment.

### Plugims/django apps
- django-taggit --- simple tagging system
- django-imagekit --- image processing library, used for all graphics hosted on blog
- mistune --- Markdone compiler, extended for awesome features

### Clean
The code is free of magic, except django.

### RSS
Blog generates RSS feeds, yay!

### Tests
There are tests, not many of them, but they make critical things intact (like not seeing unpublished posts).

#### It also has an intresting 404 page.
