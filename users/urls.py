from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/', views.another_user_profile, name='another_profile'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.friends_search_view, name='search'),
    path('friend_requests/', views.friend_requests_view, name='friend_requests'),
    path('remove_friend/<int:friend_id>/', views.remove_friend_view, name='remove_friend'),
    path('friend_list/', views.friend_list_view, name='friend_list'),
    path('followers/<int:user_id>/', views.followers_list_view, name='followers_list'),
    path('followings/<int:user_id>/', views.following_list_view, name='followings_list'),
    path('friend_requests/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend_requests/decline/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('photos/<int:user_id>/', views.user_photos_view, name='photos'),
    path('photos/set-avatar/<int:photo_id>/', views.set_avatar_view, name='set_avatar'),
    path('upload-avatar/', views.upload_avatar_view, name='upload_avatar'),
    path('toggle_like/<int:photo_id>/', views.toggle_photo_like, name='toggle_photo_like'),
    path('liked-items/', views.liked_items_view, name='liked_items'),
]
