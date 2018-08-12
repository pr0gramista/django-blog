from django.db import models
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill, ResizeCanvas
from .imagekit import UpscaleToFit

post_help_text = """
Markdown editor with some special tags:</br>
!-- makes an endash –</br>
![text][alt](img url) makes a figure</br>
!F[text][icon name][color without #][class (can be empty)](link)</br>
"""

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa")
    image = ProcessedImageField(
        upload_to='images/categories',
        verbose_name="Ikonka",
        processors=[ResizeToFill(128, 128, upscale=False)],
        format='JPEG',
        options={'quality': 80})
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    show_title = models.BooleanField(verbose_name="Pokaż tytuł", default=True)
    title_size = models.IntegerField(default=42, verbose_name="Wielkość tytułu (px)")
    title_background = models.CharField(
        max_length=80, default='rgba(0, 0, 0, 0.5)', verbose_name="Kolor tła tytułu")
    fullwidth = models.BooleanField(
        default=True, verbose_name="Pełna szerokość strony (usuwa boczny panel)")
    image = models.ForeignKey(
        'HeaderImage',
        on_delete=models.DO_NOTHING,
        verbose_name="Główny obrazek")
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="Kategoria")
    read_time = models.TextField(verbose_name="Czas czytania", default='5 minut', blank=True)
    pub_date = models.DateTimeField(verbose_name="Data publikacji")
    raw_content = models.TextField(verbose_name="Zawartość surowa", help_text=post_help_text)
    content = models.TextField(verbose_name="Zawartość", default='', blank=True)
    published = models.BooleanField(verbose_name="Opublikowany", default=False)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(default='')
    content = models.TextField(verbose_name="Zawartość")
    order = models.IntegerField(verbose_name="Kolejność", default=10)

    def __str__(self):
        return self.title


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


class HeaderImage(models.Model):
    image = ProcessedImageField(
        upload_to='images/posts',
        verbose_name="Obrazek",
        processors=[ResizeToFill(1024, 576, upscale=False), UpscaleToFit(
            512, 288), ResizeCanvas(1024, 576, color=(255, 255, 255))],
        format='JPEG',
        options={'quality': 80})
    def __str__(self):
        return self.image.name
