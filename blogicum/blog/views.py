from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Category, Post


def index(request):
    posts = Post.objects.select_related('category').filter(
        # Проверяем, что
        pub_date__lt=timezone.now(),  # Дата — не позже текущего времени;
        is_published=True,  # Пост разрешён к публикации;
        category__is_published=True  # Категория разрешена к публикации.
    ).order_by('-pub_date')[:5]
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
    posts = Post.objects.select_related('category').filter(
        # Проверяем, что
        category__slug=category_slug,
        pub_date__lt=timezone.now(),  # Дата — не позже текущего времени;
        is_published=True,  # Пост разрешён к публикации;
    )
    context = {'post_list': posts, 'category': category}
    return render(request, 'blog/category.html', context)
