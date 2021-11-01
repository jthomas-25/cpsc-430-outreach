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

def printSessionCookies(request):
    print("Session cookies = {")
    numSpaces = len("Session cookies = {")
    for key, value in request.session.items():
        print(" " * numSpaces, key, " : ", value)
    numSpaces -= 1
    print(" " * numSpaces + "}")

def deleteCookie(request, cookieName):
    try:
        del request.session[cookieName]
    except KeyError:
        #cookie doesn't exist
        pass

def getCookie(request, cookieName):
    return request.session.get(cookieName, None)

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
            result = validateUserData(email, password)
            #result = "match"
            if result == "match":
                # redirect to login success page
                response = redirect(LOGIN_SUCCESS)
                request.session["email"] = email
                request.session["account_type"] = accountType
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
    context["account"] = accountType
    response = render(request, LOGIN_PAGE, context)
    return response

def validateUserData(email, password):
    result = ""
    accounts = accountDB.getTable()
    # check if the account exists in the database
    if email not in accounts:
        result = "no account"
    else:
        account = accounts[email]
        # check if the account is blocked
        if account.getStatus() == "blocked":
            result = "blocked"
        else:
            # check if the passwords match
            result = "match" if password == account.getPassword() else "no match"
    return result

def loginSuccess(request):
    return render(request, LOGIN_SUCCESS_PAGE, {})

def logout(request):
    #if "email" not in request.session:
    #    return HttpResponseNotFound()
    response = render(request, LOGOUT_PAGE, {})
    deleteCookie(request, "email")
    deleteCookie(request, "account_type")
    #request.session.clear()
    printSessionCookies(request)
    return response

def adminHome(request):
    #if not getCookie(request, "email") or getCookie(request, "account_type") != "admin":
    #    return redirect(LOGIN_TYPE)
    return render(request, ADMIN_HOMEPAGE, {})

def studentHome(request):
    if not getCookie(request, "email") or getCookie(request, "account_type") != "student":
        return redirect(LOGIN_TYPE)
    return render(request, STUDENT_HOMEPAGE, {})

def employerHome(request):
    if not getCookie(request, "email") or getCookie(request, "account_type") != "employer":
        return redirect(LOGIN_TYPE)
    return render(request, EMPLOYER_HOMEPAGE, {})

def adminManagePosts(request):
    context = {}
    posts = []
    for post in postDB.getPosts():
        accounts.append(post)

    context["posts"] = posts
    return render(request, ADMIN_MANAGE_POSTS_PAGE, context)

def adminManageAccounts(request):
    context = {}
    accounts = []
    for account in accountDB.getAccounts():
        accounts.append(account)

    context["accounts"] = accounts
    return render(request, ADMIN_MANAGE_ACCOUNTS_PAGE, context)

def adminViewAccount(request):
    context = {}
    email = request.GET.get("email", "")
    account = accountDB.getAccountByEmail(email)
    #if request.method == "GET":
    if request.method == "POST":
        blockAccountButtonClicked = request.POST.get("Block Account", "")
        unblockAccountButtonClicked = request.POST.get("Unblock Account", "")
        deleteAccountButtonClicked = request.POST.get("Delete Account", "")
        if blockAccountButtonClicked:
            # block account, preventing user from accessing it
            accountDB.updateAccountStatus(account, "blocked")
            # redirect to manage accounts page
            return redirect(ADMIN_MANAGE_ACCOUNTS)
        elif unblockAccountButtonClicked:
            # unblock account, enabling user to access it
            accountDB.updateAccountStatus(account, "unblocked")
            # redirect to manage accounts page
            return redirect(ADMIN_MANAGE_ACCOUNTS)
        elif deleteAccountButtonClicked:
            pass
    #else:
    #    email = request.GET.get("email", "")
    #    account = accountDB.getAccountByEmail(email)
    
    context["account"] = account
    return render(request, ADMIN_VIEW_ACCOUNT_PAGE, context)

def searchPosts(request):
    response = None
    context = {}
    posts = []
    searchString = ""
    searchButtonClicked = ""
    currentFilter = ""
    if request.method == "POST":
        print(request.POST)
        searchString = request.POST.get("q", "")
        searchButtonClicked = request.POST.get("Search", "")
        currentFilter = request.POST.get("filter", "")
        request.session["search_filter"] = currentFilter
        printSessionCookies(request)
        # search for posts matching pattern %[filter]%
        posts = postDB.search(currentFilter, searchString)
        # put this in HTML
        #if len(description) > 50:
        #    description = description[:50] + "..."
        for post in posts:
            print("Title: " + post.getTitle(),
                  "Job type: " + post.getJobType(),
                  "Description: " + post.getDescription())

    context["query"] = searchString
    context["selected"] = currentFilter
    context["searchButtonClicked"] = searchButtonClicked
    context["posts"] = posts
    response = render(request, SEARCH_POSTS_PAGE, context)
    return response

def viewPost(request):
    context = {}
    post = None
    if request.method == "GET":
        postId = int(request.GET.get("postid", ""))
        post = postDB.getPostById(postId)
    
    context["post"] = post
    return render(request, VIEW_POST_PAGE, context)

def employerCreatePost(request):
    context = {}
    form = None
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            author = getCookie(request, "email")
            title = form.cleaned_data["title"]
            jobType = form.cleaned_data["jobType"]
            description = form.cleaned_data["description"]
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
        #testFile.write(post.getAuthor() + " " + getCookie(request, "email") + "\n")
        if post.getAuthor() == getCookie(request, "email"):
            posts.append(post)
    #testFile.close()

    context["posts"] = posts
    return render(request, EMPLOYER_VIEW_POSTS_PAGE, context)


setupDatabases()
