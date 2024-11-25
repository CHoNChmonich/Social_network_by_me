from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from posts.models import Post, PostImage, PostVideo ,PostLike
from users.models import Photo
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from posts.forms import PostForm

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Сохранение изображений
            for image in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=image)
            # Сохранение видео
            for video in request.FILES.getlist('videos'):
                PostVideo.objects.create(post=post, video=video)
            return redirect('posts:news_feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def news_feed_view(request):
    user = request.user
    # Собираем посты текущего пользователя, друзей и подписок
    posts = Post.objects.filter(
        models.Q(author=user) |
        models.Q(author__in=user.friends()) |
        models.Q(author__in=user.following())
    ).distinct().order_by('-created_at')
    for post in posts:
        post.is_liked = post.is_liked_by_user(request.user)
    context = {
        'posts': posts,
        'title': 'Новости',
    }
    return render(request, 'posts/news_feed.html', context)

@login_required
def repost_view(request, post_id):
    original_post = Post.objects.get(id=post_id)
    repost = Post.objects.create(
        author=request.user,
        content=original_post.content,
        is_repost=True,
        original_post=original_post  # Указываем на оригинальный пост
    )
    # Копируем изображения
    for image in original_post.images.all():
        repost_image = PostImage.objects.create(image=image.image, post = repost)  # Создаем новый объект изображения

    # Копируем видео
    for video in original_post.videos.all():
        repost_video = PostVideo.objects.create(video=video.video, post = repost)  # Создаем новый объект видео
    return redirect('users:profile')


@login_required
def delete_post_view(request, post_id):
    # Находим пост, который репостит текущий пользователь
    post = Post.objects.get(id=post_id)
    # Проверяем, что этот пост действительно является репостом
    post.delete()

    # Перенаправляем обратно на страницу профиля или ленту новостей
    return redirect('users:profile')

# Представление для лайков на постах
@login_required
def toggle_post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверяем, есть ли лайк от текущего пользователя
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)

    if not created:
        # Если лайк уже существует, удаляем его
        like.delete()

    return redirect('posts:news_feed')  # Перенаправляем на ленту новостей
