from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import mail
from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from posts.models import Post
from users.admin import CustomUserAdmin
from verify_email.email_handler import send_verification_email

# From home.templatetags import custom_tags # This line imports the templatetags file and allows use of tags
from home.templatetags import custom_tags

# Create your views here.

def user_profile(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    posts = user.posts.all()
    for post in posts:
        post.date_posted = str(post.date_posted)

    return render(request,'user_profile.html',{'user':user,'posts':posts})

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,initial={'graduation_date':None})
        if form.is_valid():
            user = form.save()

            
            #Get data from the email field
            #data = form.cleaned_data.get("email")
            
            #Check if email contains mail.umw.edu as the domain
          #  if "@mail.umw.edu" in data:
              #  pass
                #Set is_student or is_employer to True
               # inactive_user.is_student = True
                
            #If email contains anything but umw's domain, set employer to True
            #else:
            #    pass
              #  active_user.is_employer = True
            user.save()
            inactive_user = send_verification_email(request, form)
            user = inactive_user
            return redirect("/users/login")
    else:
        form = CustomUserCreationForm()
    return render(request,'user_create_form.html',{'form':form})

@login_required
def user_edit(request,id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,instance=request.user,is_student=user.is_student)
        if form.is_valid():
            user = form.save()
            request.session['email'] = user.email
            return redirect("/users/myprofile/")
    else:
        form = CustomUserChangeForm(instance=request.user,is_student=user.is_student)
    return render(request,'user_change_form.html',{'form':form})

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
            if request.session.get("email") == user.email:
                logout(request)
                user.delete()
                return HttpResponseRedirect("/")
            user.delete()
            return HttpResponseRedirect("/users/")
    
    context = {
        'user': user,
        'accountType' : accountType,
        'accountStatus': accountStatus
    }
    return render(request,'users/user_detail.html',context)

#@custom_tags.admin
def approveAccount(user):
    user.is_pending = False
    user.is_active = True
    user.is_blocked = False
    user.save()

#@custom_tags.admin
def blockAccount(user):
    user.is_pending = False
    user.is_active = False
    user.is_blocked = True
    user.save()

#@custom_tags.admin
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

    
