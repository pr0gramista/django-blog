from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from taggit.models import Tag

from .models import Post, Page


POSTS_PER_PAGE = 5


def index(request):
    return pagination(request, 1)


def pagination(request, pagination):
    page = int(pagination)
    published_posts = Post.objects.filter(published=True).order_by('-pub_date')
    paginator = Paginator(published_posts, POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)


def post(request, post_slug):
    query = Post.objects.filter(published=True)
    post = get_object_or_404(query, slug=post_slug)
    context = {'post': post}
    return render(request, 'blog/post.html', context)


def tag(request, tag_slug):
    posts = Post.objects.filter(published=True).filter(tags__slug__in=[tag_slug]).all()
    tag = Tag.objects.get(slug=tag_slug)
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/tag.html', context)


def page(request, page_slug):
    page = Page.objects.get(slug=page_slug)
    context = {'page': page}
    return render(request, 'blog/page.html', context)
