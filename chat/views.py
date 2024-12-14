from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from users.models import User


@login_required
def chat_list_view(request):
    chats = request.user.chats.all().order_by('-updated_at')  # Сортировка по последнему обновлению
    return render(request, 'chat/chat_list.html', {'chats': chats})


@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    other_users = chat.participants.exclude(id=request.user.id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
            chat.save()  # Обновление `updated_at`
        return redirect('chat:chat_detail', chat_id=chat.id)
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'other_users': other_users})


@login_required
def create_chat_view(request):
    if request.method == "POST":
        participants_ids = request.POST.getlist('participants')  # Список ID выбранных участников
        if participants_ids:
            chat = Chat.objects.create()
            chat.participants.add(request.user, *User.objects.filter(id__in=participants_ids))
            return redirect('chat:chat_detail', chat_id=chat.id)
    friends = User.objects.exclude(id=request.user.id)  # Условие "друзья" зависит от вашей логики
    return render(request, 'chat/create_chat.html', {'friends': friends})


@login_required
def create_or_redirect_chat(request, user_id):
    # Проверяем, есть ли уже чат с этим пользователем
    other_user = get_object_or_404(User, id=user_id)

    # Ищем существующий чат между текущим пользователем и выбранным
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not chat:
        # Если чат не найден, создаем новый
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
        chat.save()

    # Перенаправляем на страницу чата
    return redirect('chat:chat_detail', chat_id=chat.id)
