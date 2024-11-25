from django.contrib import admin
from posts.models import Post, PostImage, PostVideo, PostLike

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostVideo)
admin.site.register(PostLike)