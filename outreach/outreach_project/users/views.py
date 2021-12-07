from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import mail
from django.db.models import fields
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from posts.models import Post
from users.admin import CustomUserAdmin
from django_email_verification import send_email
from django.core.mail import send_mail

# From home.templatetags import custom_tags # This line imports the templatetags file and allows use of tags
from home.templatetags import custom_tags

# Create your views here.
@login_required
def user_profile(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    posts = user.posts.all()
    for post in posts:
        post.date_posted_str = post.get_date_str(post.date_posted)
    return render(request,'user_profile.html',{'user':user,'post_list':posts})

def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,initial={'graduation_date':None})
        if form.is_valid():

            user = form.save()
            user.is_active = False
            user.is_pending = True
            send_email(user)

            #Get data from the email field
            data = form.cleaned_data.get("email")
            
            #Check if email contains mail.umw.edu as the domain
            if "@mail.umw.edu" in data:
            
                pass
                #Set is_student or is_employer to True
                user.is_student = True
                
            #If email contains anything but umw's domain, set employer to True
            else:
                pass
                user.is_employer = True
            user.save()

            return redirect("/users/login")
    else:
        form = CustomUserCreationForm()
    return render(request,'user_create_form.html',{'form':form})

@login_required
def user_edit(request,id):
    if request.session['user_id'] == int(id) or request.session['is_admin']: 
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
    else:
        return HttpResponseRedirect('/','Permission Denied')

class user_login(views.LoginView):
    template_name = 'user_login_form.html'

    def form_valid(self, form):
        login(self.request,form.get_user())
        self.request.session['is_student'] = form.get_user().is_student
        self.request.session['is_employer'] = form.get_user().is_employer
        self.request.session['is_admin'] = form.get_user().is_admin
        self.request.session['user_id'] = form.get_user().id
        self.request.session['email'] = form.get_user().email
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/"
        #return "/posts/"
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#Get all users
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request,'user_list.html',{'users':users})

@login_required
def user_detail(request):#, user_id):
    user = CustomUser.objects.get(id=request.GET.get("user"))
    posts= user.posts.all()
    for post in posts:
        post.date_posted_str = post.get_date_str(post.date_posted)
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
        'accountStatus': accountStatus,
        'post_list' : posts
    }
    return render(request,'user_detail.html',context)

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

@login_required
def account_delete(request):
    user = CustomUser.objects.get(id = request.session['user_id'])
    logout(request)
    user.delete()
    return HttpResponseRedirect('/')

@login_required
def contact_user(request,id):
    if request.method== 'POST':
        post = Post.objects.get(id=id)
        to = CustomUser.objects.get(id=post.user_id_id)
        sender = CustomUser.objects.get(id=request.session['user_id'])
        print(request.POST.get('body'))

        body = 'From: ' + sender.email + '\n' + request.POST.get('body')
        try:
            send_mail(request.POST.get('subject'),body,sender.email,[to.email])
            return HttpResponse('Success!')
        except(e):
            return HttpResponse("Unsuccesful")

    return render(request,'contact_user.html')

