from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('news/', views.news_feed_view, name='news_feed'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('posts/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('post/detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('repost/<int:post_id>/', views.repost_view, name='repost'),
    path('like/<int:post_id>/', views.toggle_post_like, name='toggle_post_like'),

]
