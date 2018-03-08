from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views, feeds

urlpatterns = [
    url(r'^$', views.index, name='index'),
                  url(r'^(?P<pagination>[0-9]+)/$', views.index_pagination, name='index_pagination'),
    url(r'^post/(?P<post_slug>[aA-zZ0-9-]+)/$', views.post, name='post'),
    url(r'^page/(?P<page_slug>[aA-zZ0-9-]+)/$', views.page, name='page'),
                  url(r'^tag/(?P<tag_slug>[aA-zZ0-9-]+)/(?P<pagination>[0-9]+)/$', views.tag_pagination,
                      name='tag_pagination'),
    url(r'^tag/(?P<tag_slug>[aA-zZ0-9-]+)/$', views.tag, name='tag'),
    url(r'^rss/$', feeds.LatestPostsFeed(), name='rss_index'),
    url(r'^tag/(?P<tag_slug>[aA-zZ0-9-]+)/rss/$', feeds.TagPostsFeed(), name='rss_tag'),
    url(r'^youtube$', views.youtube, name='youtube')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
