from django.shortcuts import render, redirect


# Create your views here.

def main_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
    context = {
        'title': 'Приветственная страница',
    }
    return render(request, 'main/home.html', context)