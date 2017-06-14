from django.db import models
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    show_title = models.BooleanField(verbose_name="Pokaż tytuł", default=True)
    title_size = models.IntegerField(default=42, verbose_name="Wielkość tytułu (px)")
    title_background = models.CharField(max_length=80, default='rgba(0, 0, 0, 0.5)', verbose_name="Kolor tła tytułu")
    image = ProcessedImageField(
        upload_to='images/posts',
        default='',
        verbose_name="Główny obrazek",
        processors=[ResizeToFill(1024, 576)],
        format='JPEG',
        options={'quality': 80})
    pub_date = models.DateTimeField(verbose_name="Data publikacji")
    raw_content = models.TextField(verbose_name="Zawartość surowa")
    content = models.TextField(verbose_name="Zawartość", default='', blank=True)
    published = models.BooleanField(verbose_name="Opublikowany", default=False)
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
    image = ProcessedImageField(
        upload_to='images/social_links',
        default='',
        verbose_name="Ikona",
        processors=[ResizeToFit(300, 300)],
        format='PNG')
    order = models.IntegerField(verbose_name="Kolejność", default=10)
