from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

def index(request):
    latest_posts = Post.objects.order_by('-pub_date')[:5]
    context = {'posts': latest_posts}
    return render(request, 'blog/index.html', context)

def post(request, post_slug):
    post = Post.objects.get(slug=post_slug)
    context = {'post': post}
    return render(request, 'blog/post.html', context)
