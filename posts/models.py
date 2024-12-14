from django.db import models
from users.models import User, Photo
from django.utils import timezone


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    is_repost = models.BooleanField(default=False)
    original_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='reposts')

    def like_count(self):
        return self.likes.count()

    # Проверка, поставил ли пользователь лайк
    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    def __str__(self):
        if self.original_post:
            return f"Repost by {self.author.username} of post {self.original_post.id}"
        return f"Post by {self.author.username}"

    def repost_count(self):
        return self.reposts.count()

    class Meta:
        ordering = ['-created_at']


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images/")

    def __str__(self):
        return f"Изображение для поста {self.post.id}"


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="post_videos/")

    def __str__(self):
        return f"Видео для поста {self.post.id}"


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"
