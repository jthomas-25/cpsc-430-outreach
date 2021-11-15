from django import forms
from django.forms import widgets
from django.forms.widgets import HiddenInput
from .models import Post
from django.urls import reverse_lazy

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status','user_id', 'date_posted']
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = "__all__"
        exclude = ['status','user_id', 'date_posted']
        widgets = {
            'user_id':forms.HiddenInput(),
            'date_posted':forms.DateInput()
        }
        success_url = reverse_lazy('posts/')
    


