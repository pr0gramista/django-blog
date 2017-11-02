from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

from .models import Post, Page


POSTS_PER_PAGE = 5


def index(request):
    """Displays first page with latest posts"""
    return index_pagination(request, 1)


def index_pagination(request, pagination):
    """Displays n-th page with latest posts"""
    page = int(pagination)
    if not request.user.is_authenticated:
        posts_published = Post.objects.filter(published=True).order_by('-pub_date')
    else:
        posts_published = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts_published, POSTS_PER_PAGE)

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
    """Displays single post"""
    if not request.user.is_authenticated:
        query = Post.objects.filter(published=True)
    else:
        query = Post.objects.all()
    post = get_object_or_404(query, slug=post_slug)
    context = {'post': post}
    return render(request, 'blog/post.html', context)


def tag(request, tag_slug):
    """Displays first page with posts with given tag"""
    return tag_pagination(request, tag_slug, 1)


def tag_pagination(request, tag_slug, pagination):
    """Displays n-th page with posts with given tag"""
    page = int(pagination)
    if not request.user.is_authenticated:
        posts_with_tag = Post.objects.filter(published=True).filter(tags__slug__in=[tag_slug]).order_by('-pub_date').all()
    else:
        posts_with_tag = Post.objects.filter(tags__slug__in=[tag_slug]).order_by('-pub_date').all()
    paginator = Paginator(posts_with_tag, POSTS_PER_PAGE)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    tag = Tag.objects.get(slug=tag_slug)
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'blog/tag.html', context)


def page(request, page_slug):
    """Displays page"""
    page = Page.objects.get(slug=page_slug)
    context = {'page': page}
    return render(request, 'blog/page.html', context)
