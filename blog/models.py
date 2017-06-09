from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    pub_date = models.DateTimeField(verbose_name="Data publikacji")
    raw_content = models.TextField(verbose_name="Zawartość surowa")
    content = models.TextField(verbose_name="Zawartość", default='')
    tags = TaggableManager()

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    content = models.TextField(verbose_name="Zawartość")
    order = models.IntegerField(verbose_name="Kolejność", default=10)

class SocialLink(models.Model):
    slug = models.SlugField(default='')
    tooltip = models.CharField(max_length=200, verbose_name="Podpis")
    url = models.URLField(verbose_name="Adres linku")
    image = models.ImageField(verbose_name="Ikona")
    order = models.IntegerField(verbose_name="Kolejność", default=10)
