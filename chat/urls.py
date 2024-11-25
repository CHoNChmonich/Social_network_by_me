from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chats/', views.chat_list_view, name='chat_list'),
    path('chats/<int:chat_id>/', views.chat_detail_view, name='chat_detail'),
    path('chats/create/', views.create_chat_view, name='create_chat'),
    path('chats/other_user/<int:user_id>/', views.create_or_redirect_chat, name='create_or_redirect_chat'),
]
