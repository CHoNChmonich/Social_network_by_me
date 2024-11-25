from django import forms
from .models import Post, PostImage, PostVideo


class PostForm(forms.ModelForm):
    images = forms.FileField(widget=forms.FileInput(), required=False)
    videos = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Post
        fields = ['content', 'images', 'videos']