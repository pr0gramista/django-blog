from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.CharField(max_length=200, default='')
    pub_date = models.DateTimeField(verbose_name="Data publikacji")
    tags = TaggableManager()
    content = models.TextField(verbose_name="Zawartość")
    compiled_content = models.TextField(verbose_name="Zawartość skompilowana", default='')
