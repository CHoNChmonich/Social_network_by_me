from django.contrib import auth
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Photo, Album, PhotoLike
from .forms import PhotoUploadForm, RegistrationForm, UserEditForm, PhotoForm, AvatarUploadForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, User
from posts.models import PostLike
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.db import models
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создание пользователя
            user = form.save()
            # Аутентификация и вход пользователя
            login(request, user)
            return redirect('users:profile')  # Перенаправление на домашнюю страницу или куда необходимо
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user=form.get_user()
            if user:
                login(request, user)
                return redirect('users:profile')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    context = {
        'title': 'Страница авторизации',
        'form': form,
    }
    return render(request, 'users/login.html', context)

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photo_gallery')
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})

@login_required
def photo_gallery(request):
    photos = Photo.objects.filter(user=request.user)
    return render(request, 'photos/gallery.html', {'photos': photos})

@login_required
def profile(request):
    user = request.user
    avatar_image = Photo.objects.filter(user=request.user, is_avatar=True).first()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('users:profile')
    else:
        form = PhotoForm()
    friends_count = user.friends_count()
    followers_count = user.followers_count()
    followings_count = user.following_count()
    context = {
        'title': 'Профиль пользователя',
        'user': user,
        'friends_count': friends_count,
        'followers_count': followers_count,
        'followings_count': followings_count,
        'form': form,
        'avatar': avatar_image,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваши данные успешно обновлены!")
            return redirect('users:profile')
    else:
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
        'title': "Редактирование профиля",
    }
    return render(request, 'users/edit_profile.html', context)

def another_user_profile(request, user_id):
    # Получаем пользователя по его id
    user = User.objects.get(id=user_id)
    friends_count = user.friends_count()
    followers_count = user.followers_count()
    # Получаем текущего пользователя
    current_user = request.user

    # Проверяем, есть ли у текущего пользователя запрос в друзья от этого пользователя
    friend_request = FriendRequest.objects.filter(
        from_user=user, to_user=current_user, is_accepted=False).first()

    # Проверяем, есть ли у текущего пользователя запрос в друзья, который он отправил этому пользователю
    received_request = FriendRequest.objects.filter(
        from_user=current_user, to_user=user, is_accepted=False).first()

    # Проверяем, является ли текущий пользователь другом этого пользователя
    is_friend = user.friends().filter(id=current_user.id).exists()

    # Формируем контекст
    context = {
        'user': user,
        'is_friend': is_friend,
        'friend_request': friend_request,
        'received_request': received_request,
    }

    return render(request, 'users/another_user_profile.html', context)

@login_required
def friend_requests_view(request):
    incoming_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    outgoing_requests = FriendRequest.objects.filter(from_user=request.user, is_accepted=False)

    context = {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'title': 'Запросы в друзья',
    }
    return render(request, 'users/friend_requests.html', context)

@login_required
def friend_list_view(request):
    user = request.user
    friends = user.friends()  # Используем метод friends() модели User
    context = {
        'title': 'Список друзей',
        'friends': friends,
    }
    return render(request, 'users/friend_list.html', context)

@login_required
def followers_list_view(request, user_id):
    user = User.objects.get(id=user_id)
    incoming_requests = FriendRequest.objects.filter(to_user=user, is_accepted=False)
    # Вызов метода followers из модели User
    context = {
        'profile_user': user,
        'incoming_requests': incoming_requests,
    }
    return render(request, 'users/followers_list.html', context)

@login_required
def following_list_view(request, user_id):
    user = User.objects.get(id=user_id)
    followings = user.following()  # Вызов метода followers из модели User
    context = {
        'profile_user': user,
        'followings': followings,
    }
    return render(request, 'users/following_list.html', context)

@login_required
def send_friend_request(request, user_id):
    # Получаем пользователя, которому отправляется запрос
    to_user = get_object_or_404(User, pk=user_id)
    from_user = request.user

    # Проверяем, не является ли текущий пользователь уже другом
    if to_user.friends().filter(id=from_user.id).exists():
        return redirect('users:profile', user_id=user_id)  # Если уже друг, то возвращаемся на страницу профиля

    # Проверяем, не был ли уже отправлен запрос
    existing_request = FriendRequest.objects.filter(
        from_user=from_user, to_user=to_user, is_accepted=False).first()

    if not existing_request:
        # Создаем новый запрос
        FriendRequest.objects.create(
            from_user=from_user, to_user=to_user, is_accepted=False)

    return redirect('users:profile')  # Перенаправляем на профиль


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.is_accepted = True
    friend_request.save()
    return redirect('users:friend_requests')

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    return redirect('users:friend_requests')

@login_required
def remove_friend_view(request, friend_id):
    friend = User.objects.get(id=friend_id)

    # Удаляем дружбу из отправленных и полученных запросов
    FriendRequest.objects.filter(
        (models.Q(from_user=request.user, to_user=friend) |
         models.Q(from_user=friend, to_user=request.user)),
        is_accepted=True
    ).delete()

    return redirect('users:friend_list')

def friends_search_view(request):
    users = User.objects.annotate(
        friends_count=Count(
            'sent_requests',
            filter=Q(sent_requests__is_accepted=True)
        ) + Count(
            'received_requests',
            filter=Q(received_requests__is_accepted=True)
        )
    ).order_by('-friends_count')[:10]
    context = {
        'title': 'Поиск друзей',
        'users': users,
    }
    return render(request, 'users/friends_search.html', context)

@login_required
def user_photos_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    photos = Photo.objects.filter(user=user).order_by('-uploaded_at')
    for photo in photos:
        photo.is_liked = photo.is_liked_by_user(request.user)

    context = {
        'profile_user': user,
        'photos': photos,
    }
    return render(request, 'users/user_photos.html', context)

@login_required
def set_avatar_view(request, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id, user=request.user)
    except Photo.DoesNotExist:
        return redirect('users:photos')  # Если фото не найдено, возвращаем пользователя на страницу фотографий

    # Сброс флага `is_avatar` для всех фотографий пользователя
    Photo.objects.filter(user=request.user, is_avatar=True).update(is_avatar=False)

    # Установка нового аватара
    photo.is_avatar = True
    photo.save()

    return redirect('users:profile')

@login_required
def upload_avatar_view(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Сбрасываем текущий аватар, если он есть
            Photo.objects.filter(user=request.user, is_avatar=True).update(is_avatar=False)

            # Создаем новую фотографию и устанавливаем её как аватар
            avatar_photo = form.save(commit=False)
            avatar_photo.user = request.user
            avatar_photo.is_avatar = True
            avatar_photo.save()

            return redirect('users:profile')  # Перенаправляем на профиль
    else:
        form = AvatarUploadForm()

    return render(request, 'users/upload_avatar.html', {'form': form})

@login_required
def toggle_photo_like(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    # Проверяем, поставил ли пользователь лайк
    like, created = PhotoLike.objects.get_or_create(user=request.user, photo=photo)

    if not created:
        # Если лайк уже существует, удаляем его
        like.delete()

    return redirect('users:profile')  # Перенаправляем на страницу профиля или другую страницу

@login_required
def liked_items_view(request):
    # Получаем все лайки для постов и фотографий пользователя
    post_likes = PostLike.objects.filter(user=request.user).order_by('-created_at')
    photo_likes = PhotoLike.objects.filter(user=request.user).order_by('-created_at')

    # Объединяем лайки
    all_likes = list(post_likes) + list(photo_likes)

    # Сортируем объединённые лайки по дате создания
    all_likes.sort(key=lambda x: x.created_at, reverse=True)

    # Добавляем тип объекта для каждого лайка
    liked_items = []
    for like in all_likes:
        item_type = 'Post' if isinstance(like, PostLike) else 'Photo'
        liked_items.append({'like': like, 'item_type': item_type})

    return render(request, 'users/liked_items.html', {'liked_items': liked_items})



