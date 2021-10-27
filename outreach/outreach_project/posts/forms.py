from django import forms
from .models import Post
from django.urls import reverse_lazy

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        success_url = reverse_lazy('posts/')