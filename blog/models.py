from django.db import models
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToCover
from colorfield.fields import ColorField

class Post(models.Model):
    COVER = 'cover'
    CONTAIN = 'contain'
    IMAGE_STATEGY = {
        (COVER, 'cover'),
        (CONTAIN, 'contain')
    }

    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    show_title = models.BooleanField(verbose_name="Pokaż tytuł", default=True)
    title_background = ColorField(default='#000', verbose_name="Kolor tła tytułu")
    title_background_opacity = models.FloatField(default='0.5', verbose_name="Przeźroczystość tła tytułu")
    image = ProcessedImageField(
        upload_to='images/posts',
        default='',
        verbose_name="Główny obrazek",
        processors=[ResizeToCover(800, 600)],
        format='JPEG',
        options={'quality': 80})
    image_display_stategy = models.CharField(max_length=30, choices=IMAGE_STATEGY, default=COVER, verbose_name="Stategia wielkości tła")
    image_background = ColorField(default='#FFF', verbose_name="Kolor tła obrazka", blank=True)
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
