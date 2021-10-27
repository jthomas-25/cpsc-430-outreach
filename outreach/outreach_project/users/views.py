from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render

from users.admin import CustomUserAdmin
from.models import CustomUser
from django.views.generic import CreateView
from django.contrib.auth import views
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model,login,logout

# Create your views here.

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/users/login")
    else:
        form = CustomUserCreationForm()
    return render(request,'user_create_form.html',{'form':form})

def user_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            form = CustomUserChangeForm()
    return render(request,'user_create_form.html',{'form':form})

#class user_create(CreateView):
#    model = get_user_model()
#    fields = ['email','password']
#    form = CustomUserCreationForm
#    template_name = 'user_create_form.html'
#    success_url = "/"

class user_login(views.LoginView):
    template_name = 'user_login_form.html'

    def form_valid(self, form):
        login(self.request,form.get_user())
        self.request.session['user_id'] = form.get_user().id
        self.request.session['email'] = form.get_user().email
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/posts/"

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
