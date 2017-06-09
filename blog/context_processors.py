from django.http import HttpRequest

from .models import Page, SocialLink

def page_list(request):
    return {
        "pages": Page.objects.order_by('order')
    }

def social_links(request):
    return {
        "social_links": SocialLink.objects.order_by('order')
    }
