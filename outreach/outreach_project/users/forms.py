from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import CustomUserManager

from .models import  CustomUser


class CustomUserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True,help_text="Enter a valid email")
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)
        

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['email']
