from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from users.utils import get_avatar_upload_path

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    about = models.TextField(blank=True, null=True, verbose_name="Хобби")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.username

    def friends(self):
        # Все друзья, где запросы приняты
        return User.objects.filter(
            models.Q(sent_requests__to_user=self, sent_requests__is_accepted=True) |
            models.Q(received_requests__from_user=self, received_requests__is_accepted=True)
        )

    def followers(self):
        # Возвращает пользователей, которые отправили запросы текущему пользователю
        return User.objects.filter(
            sent_requests__to_user=self, sent_requests__is_accepted=False
        )

    def following(self):
        # Пользователи, которым отправил запросы
        return User.objects.filter(
            received_requests__from_user=self, received_requests__is_accepted=False
        )

    def friends_count(self):
        return self.friends().count()

    def followers_count(self):
        return self.followers().count()

    def following_count(self):
        return self.following().count()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_requests",
        verbose_name="Отправитель"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_requests",
        verbose_name="Получатель"
    )
    is_accepted = models.BooleanField(default=False, verbose_name="Принято ли")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        unique_together = ('from_user', 'to_user')  # Запрет на дублирование запросов

    def __str__(self):
        status = "Принят" if self.is_accepted else "В ожидании"
        return f"{self.from_user} → {self.to_user} ({status})"


class Album(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name="Пользователь"
    )
    name = models.CharField(max_length=255, verbose_name="Название альбома")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Пользователь"
    )
    album = models.ForeignKey(
        'Album',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='photos',
        verbose_name="Альбом"
    )
    image = models.ImageField(upload_to=get_avatar_upload_path, verbose_name="Фотография")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    is_avatar = models.BooleanField(default=False, verbose_name="Аватарка")

    def like_count(self):
        return self.likes.count()

    # Проверка, поставил ли пользователь лайк
    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return f"Фото {self.id} пользователя {self.user.username}"

class PhotoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.photo}"

    class Meta:
        unique_together = ('user', 'photo')  # Запрещаем ставить несколько лайков на одну фотографию

