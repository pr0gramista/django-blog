from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post, Page

def index(request):
    latest_posts = Post.objects.filter(published=True).order_by('-pub_date')[:5]
    context = {'posts': latest_posts}
    return render(request, 'blog/index.html', context)

def post(request, post_slug):
    query = Post.objects.filter(published=True)
    post = get_object_or_404(query, slug=post_slug)
    context = {'post': post}
    return render(request, 'blog/post.html', context)

def page(request, page_slug):
    page = Page.objects.get(slug=page_slug)
    context = {'page': page}
    return render(request, 'blog/page.html', context)
