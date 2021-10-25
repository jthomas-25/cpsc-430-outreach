from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from .forms import *
from .models import *
from .pages import *
from .urls import *

accountFactory = AccountFactory()
#these will be replaced by SQLite databases
accountDB = AccountDatabase()
postDB = PostDatabase()

def setupDatabases():
    student = accountFactory.create("student", "student@mail.umw.edu", "password")
    employer = accountFactory.create("employer", "employer@gmail.com", "password")
    admin = accountFactory.create("admin", "admin@mail.umw.edu", "password")
    accountDB.addAccount(student)
    accountDB.addAccount(employer)
    accountDB.addAccount(admin)
    post = Post("John", "Test Post", "Tutoring", "This is a test")
    postDB.addPost(post)

def index(request):
    return render(request, INDEX_PAGE, {})

def loginType(request):
    return render(request, LOGIN_TYPE_PAGE, {})

def login(request):
    # no account type parameter
    if "account" not in request.GET:
        return HttpResponseNotFound()

    response = None
    context = {}
    form = None
    email = ""
    accountType = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            accountType = request.GET.get("account", "")
            result = validateUserData(email, password, accountDB.getAccounts())
            #result = "match"
            if result == "match":
                # redirect to login success page
                response = redirect(LOGIN_SUCCESS)
                response.set_cookie("email", email)
                response.set_cookie("account_type", accountType)
                return response
            else: 
                context["result"] = result
        else:
            # blank form
            form = LoginForm()
    else:
        # blank form
        form = LoginForm()

    context["form"] = form
    context["account"] = request.GET.get("account", "")
    response = render(request, LOGIN_PAGE, context)
    return response

def validateUserData(email, password, accounts):
    result = ""
    # check if the account exists in the database
    if email not in accounts:
        result = "no account"
    else:
        accountPassword = accounts[email].getPassword()
        # check if the passwords match
        result = "match" if password == accountPassword else "no match"
    return result

def loginSuccess(request):
    return render(request, LOGIN_SUCCESS_PAGE, {})

def logout(request):
    if "email" not in request.COOKIES:
        return HttpResponseNotFound()
    response = HttpResponse()
    response.delete_cookie("email")
    return render(request, LOGOUT_PAGE, {})

def studentHome(request):
    return render(request, STUDENT_HOMEPAGE, {})

def employerHome(request):
    return render(request, EMPLOYER_HOMEPAGE, {})

def adminHome(request):
    return render(request, ADMIN_HOMEPAGE, {})

def searchPosts(request):
    #params = request.GET.copy()
    context = {}
    posts = []
    searchString = ""
    searchButton = ""
    if request.method == "POST":
        searchString = request.POST.get("q", "")
        searchButton = request.POST.get("Search", "")
        # search for posts by title, matching pattern %[title]%
        for post in postDB.getPosts():
            if searchString == post.getTitle():
                posts.append(post)
        context["posts"] = posts
        context["searchButton"] = searchButton

    context["query"] = searchString
    return render(request, SEARCH_POSTS_PAGE, context)


def employerCreatePost(request):
    context = {}
    form = None
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            author = request.COOKIES["email"]
            title = form.cleaned_data["title"]
            jobType = form.cleaned_data["jobType"]
            description = form.cleaned_data["description"]
            if len(description) > 50:
                description = description[:50] + "..."
            post = Post(author, title, jobType, description)
            postDB.addPost(post)
            with open("job_board/testFile.txt", "w") as testFile:
                testFile.write("Number of posts: " + str(postDB.size()) + "\n")
            # redirect to post submitted page
            return redirect(POST_SUBMITTED)
        else:
            #blank form
            form = CreatePostForm()
    else:
        #blank form
        form = CreatePostForm()
    
    context["form"] = form
    return render(request, CREATE_POST_PAGE, context)

def postSubmitted(request):
    return render(request, POST_SUBMITTED_PAGE, {})

def employerViewPosts(request):
    context = {}
    posts = []
    #testFile = open("job_board/testFile.txt", "a")
    for post in postDB.getPosts():
        #testFile.write(post.getAuthor() + " " + request.COOKIES["email"] + "\n")
        if post.getAuthor() == request.COOKIES["email"]:
            posts.append(post)
    #testFile.close()

    context["posts"] = posts
    return render(request, EMPLOYER_VIEW_POSTS_PAGE, context)


setupDatabases()
