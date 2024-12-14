from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Photo, User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'image', 'description']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Введите почту'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    phone_number = forms.CharField(max_length=15, required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'about', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Загрузить фото',
        }


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
