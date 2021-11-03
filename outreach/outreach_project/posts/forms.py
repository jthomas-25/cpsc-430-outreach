from django import forms
from django.forms import widgets
from django.forms.widgets import HiddenInput
from .models import Post
from django.urls import reverse_lazy

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status','user_id']
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status','user_id']
        widgets = {'user_id':forms.HiddenInput()}
        success_url = reverse_lazy('posts/')
