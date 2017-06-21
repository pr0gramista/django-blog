from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<pagination>[1-9]+)/$', views.pagination, name='pagination'),
    url(r'^post/(?P<post_slug>[aA-zZ0-9-]+)/$', views.post, name='post'),
    url(r'^page/(?P<page_slug>[aA-zZ0-9-]+)/$', views.page, name='page'),
    url(r'^tag/(?P<tag_slug>[aA-zZ0-9-]+)/$', views.tag, name='tag')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
