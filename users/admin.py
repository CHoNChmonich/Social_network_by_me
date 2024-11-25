from django.contrib import admin
from users.models import User, FriendRequest, Album, Photo
# Register your models here.
admin.site.register(User)
admin.site.register(FriendRequest)

admin.site.register(Album)
admin.site.register(Photo)