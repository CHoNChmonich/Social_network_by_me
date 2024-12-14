from django.urls import path

from main.views import main_view


app_name = 'main'

urlpatterns = [
    path('', main_view, name='index'),
]
