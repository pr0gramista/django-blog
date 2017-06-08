from django.http import HttpRequest

from .models import Page

def page_list(request):
    return {
        "pages": Page.objects.order_by('order')
    }
