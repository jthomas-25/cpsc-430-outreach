from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .managers import CustomUserManager

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True,help_text="Enter a valid email")
    graduation_date = forms.DateField(required=False,widget=forms.SelectDateWidget())
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',"graduation_date",'bio')
        widgets = {
            'graduation_date':forms.SelectDateWidget(
                empty_label=("Choose Year","Choose Month","Choose Day"))
            }
        
        

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['email','graduation_date','bio']
        widgets = {
            'graduation_date':forms.SelectDateWidget(
                empty_label=("Choose Year","Choose Month","Choose Day"))
            }
    def __init__(self,*args,**kwargs):
        is_student = kwargs.pop('is_student')
        super(CustomUserChangeForm,self).__init__(*args,**kwargs)
        if not is_student:
            del self.fields['graduation_date']
