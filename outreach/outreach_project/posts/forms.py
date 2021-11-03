from django import forms
from .models import Post
from django.urls import reverse_lazy

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status']
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status']
        success_url = reverse_lazy('posts/')
