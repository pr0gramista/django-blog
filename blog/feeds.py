from django.contrib.syndication.views import Feed
from django.urls import reverse
from taggit.models import Tag

from .models import Post


class LatestPostsFeed(Feed):
    title = "PR0GRAMISTA"
    link = "/rss/"
    description = "Ostatnie posty na blogu PR0GRAMISTA.pl"

    def items(self):
        return Post.objects.order_by('-pub_date').all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_link(self, item):
        return reverse('post', args=[item.slug])


class TagPostsFeed(Feed):
    def get_object(self, request, tag_slug):
        return Tag.objects.get(slug=tag_slug)

    def items(self, obj):
        return Post.objects.filter(published=True).filter(tags__slug__in=[obj.slug]).order_by('-pub_date').all()

    def link(self, obj):
        return "/tag/%s/rss" % obj.slug

    def title(self, obj):
        return "%s | PR0GRAMISTA" % obj.name

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.pub_date

    def item_link(self, item):
        return reverse('post', args=[item.slug])
