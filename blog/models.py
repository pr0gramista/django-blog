from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.CharField(max_length=200, default='')
    pub_date = models.DateTimeField(verbose_name="Data publikacji")
    tags = TaggableManager()
    raw_content = models.TextField(verbose_name="Zawartość surowa")
    content = models.TextField(verbose_name="Zawartość", default='')

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    order = models.IntegerField(verbose_name="Kolejność", default=10)
    slug = models.CharField(max_length=200, default='')
    content = models.TextField(verbose_name="Zawartość")
