from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_slug>[aA-zZ0-9-]+)/$', views.post, name='post')
]
