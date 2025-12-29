from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post
from .utils import get_published_posts

SORT_BY_PUB_DATE = '-pub_date'


def index(request):
    posts = get_published_posts().order_by(SORT_BY_PUB_DATE)[:5]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    category = post.category
    if (not post.is_published) or (not category.is_published
                                   ) or (post.pub_date > timezone.now()):
        raise Http404("Ошибка 404")
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована")
    posts = get_published_posts(category_slug)
    context = {'post_list': posts, 'category': category}
    return render(request, 'blog/category.html', context)
