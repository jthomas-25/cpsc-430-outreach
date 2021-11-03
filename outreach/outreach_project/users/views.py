from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render

from users.admin import CustomUserAdmin
from .models import CustomUser
from django.views.generic import CreateView
from django.contrib.auth import views
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_profile(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    posts = user.posts.all()

    return render(request,'user_profile.html',{'user':user,'posts':posts})

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #accountType = request.GET.get("account-type")
            #request.session['account type'] = accountType
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

#Get all users
def user_list(request):
    users = CustomUser.objects.all()
    return render(request,'users/user_list.html',{'users':users})

@login_required
def user_detail(request):#, user_id):
    user = CustomUser.objects.get(id=request.GET.get("user"))
    #user = CustomUser.objects.get(id=user_id)
    accountType = getAccountType(user)
    accountStatus = getAccountStatus(user)

    if request.method == "POST":
        approveAccountButtonClicked = request.POST.get("Approve Account")
        blockAccountButtonClicked = request.POST.get("Block Account")
        unblockAccountButtonClicked = request.POST.get("Unblock Account")
        deleteAccountButtonClicked = request.POST.get("Delete Account")
        if approveAccountButtonClicked:
            approveAccount(user)
        elif blockAccountButtonClicked:
            blockAccount(user)
        elif unblockAccountButtonClicked:
            unblockAccount(user)
        elif deleteAccountButtonClicked:
            user.delete()
    
    context = {
        'user': user,
        'accountType' : accountType,
        'accountStatus': accountStatus
    }
    return render(request,'users/user_detail.html',context)

def approveAccount(user):
    user.is_pending = False
    user.is_active = True
    user.is_blocked = False
    user.save()

def blockAccount(user):
    user.is_pending = False
    user.is_active = False
    user.is_blocked = True
    user.save()

def unblockAccount(user):
    approveAccount(user)

def getAccountType(user):
    accountType = ""
    if user.is_admin:
        accountType = "admin"
    elif user.is_student:
        accountType = "student"
    elif user.is_employer:
        accountType = "employer"
    return accountType

def getAccountStatus(user):
    accountStatus = ""
    if user.is_pending:
        accountStatus = "pending"
    elif user.is_active:
        accountStatus = "active"
    elif user.is_blocked:
        accountStatus = "blocked"
    return accountStatus


