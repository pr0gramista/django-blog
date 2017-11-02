from django.conf import settings

from .models import Page, SocialLink, Post

# Remember to add new function to TEMPLATES in settings

def page_list(request):
    return {
        "pages": Page.objects.order_by('order')
    }


def tags_list(request):
    return {
        "tags": Post.tags.most_common()[:5]
    }


def social_links(request):
    return {
        "social_links": SocialLink.objects.order_by('order')
    }


def analytics(request):
    return {
        "analytics": settings.ANALYTICS
    }
