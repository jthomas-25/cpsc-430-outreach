from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView, FormView, CreateView, UpdateView
from .forms import PostEditForm, PostCreateForm
from .models import Post
from users.models import CustomUser
import datetime
from django.utils import timezone
from datetime import time, timedelta

from django.db.models import Q

# From home.templatetags import custom_tags # This line imports the templatetags file and allows use of tags
# Type @custom_tags.student, @custom_tags.employer, @custom_tags.admin in front of function.  NOT TESTED YET
from home.templatetags import custom_tags

# Create your views here.

#Get all posts
@login_required
def post_list(request):
    posts = Post.objects.all()
    user = CustomUser.objects.get(id=request.session.get('user_id'))
    context = {
        'post_list' : posts,
        'user' : user
    }
    return render(request,"posts/post_list.html",context)

@login_required
#@custom_tags.employer
def post_mine(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    posts = user.posts.all()
    context = {'post_list':posts,'user':user}
    return render(request,'posts/post_mine.html',context)

#Get specific info for post
@login_required
def post_detail(request,id):
    post = Post.objects.get(id=id)
    user = CustomUser.objects.get(id=request.session.get('user_id'))
    
    
    if request.method == "POST":
        if user.is_admin or user.id == post.user_id_id:
            editPostButtonClicked = request.POST.get("Edit Post")
            deletePostButtonClicked = request.POST.get("Delete Post")
            if editPostButtonClicked:
                return redirect("/posts/edit/" + str(post.id))
            elif deletePostButtonClicked:
                return redirect("/posts/delete/" + str(post.id))

        # if admin reviewed post
        if user.is_admin:
            approvePostButtonClicked = request.POST.get("Approve Post")
            denyPostButtonClicked = request.POST.get("Deny Post")
            blockPostButtonClicked = request.POST.get("Block Post")
            unblockPostButtonClicked = request.POST.get("Unblock Post")
            if approvePostButtonClicked:
                post.status = "active"
                post.save()
            elif denyPostButtonClicked:
                post.delete()
                return redirect("/")
            elif blockPostButtonClicked:
                post.status = "blocked"
                post.save()
            elif unblockPostButtonClicked:
                post.status = "active"
                post.save()
            #post.save()

    context = {
        'post_detail' : post,
        'user' : user
    }
    return render(request,"posts/post_detail.html",context)

#Delete Post View
#@admin
#@employer
class post_delete(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'post_confirm_delete.html'
    raise_exception = True
    permission_denied_message = "You are not allowed here!"

    def get_object(self,queryset=None):
        obj = Post.objects.get(id=self.kwargs['id'])
        return obj
    def handle_no_permission(self):
        return redirect("/users/login/")

#Post Edit View
#@custom_tags.admin
#@custom_tags.employer
class post_edit(UpdateView, LoginRequiredMixin):
    model = Post
    template_name = 'post_edit_form.html'
    fields = '__all__'
    raise_exception = True
    permission_denied_message = "You are not allowed here!"
    success_url="/posts"

    def get_object(self,queryset=None):
        obj = Post.objects.get(id=self.kwargs['id'])
        return obj
    def handle_no_permission(self):
        return redirect("/users/login/")


@login_required
#@employer
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.instance.user_id = CustomUser.objects.get(id=request.session['user_id'])
            form.save()
            return redirect("/posts")
    else:
        form = PostCreateForm()
    return render(request,'post_create_form.html',{'form':form})

#Search 2
@login_required
def search2(request):
    query = request.GET.get('q')
    filter = request.GET.get('f')
    sort_date = request.GET.get('d')
    date_range = timezone.now()
    if sort_date == "lastday":
        date_range -= timedelta(days=1)
    elif sort_date=="lastweek":
        date_range -= timedelta(days=7)
    elif sort_date=="lastmonth":
        date_range -= timedelta(days=30)

    results = "empty"
    context={'results':results,'last_search':query,'last_filter':filter,'last_date':sort_date}
    if query == None:
        context['last_search'] = "Search..."
        context['last_filter'] = "None"
        return render(request,'search2.html',context)
    if query == "":
        results = Post.objects.all()
        if sort_date != "none":
            results = results.filter(date_posted__gte=date_range)
        context['results'] = results
        return render(request,'search2.html',context)

    if filter == "none":
        results = Post.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query) | Q(job_type__icontains=query)
        )
        context['results'] = results
    elif filter == "title":
        results = Post.objects.filter(
            Q(title__icontains=query)
        )
        context['results'] = results
    elif filter == "description":
        results = Post.objects.filter(
            Q(description__icontains=query)
        )
        context['results'] = results
    elif filter == "type":
        results = Post.objects.filter(
            Q(job_type__icontains=query)
        )
        context['results'] = results

    if sort_date != "none":
        context['results'] = results.filter(date_posted__gte=date_range)

    if len(results) == 0:
        context['results']="no_results"


    return render(request,'search2.html',context)

#Search for posts
@login_required
def search_posts(request):
    context = {}
    searchType = ""
    searchButtonClicked = ""
    posts = []

    if request.method == "POST":
        print("request.POST = {")
        for key, value in request.POST.items():
            print(" " * 4 + key + ": " + str(value))
        print("}")
        searchType = request.POST.get("search-type")
        if searchType == "Keyword":
            context['showSearchBar'] = True
            context['showDateRange'] = False
            searchButtonClicked = request.POST.get("Search")
            if searchButtonClicked:
                searchString = request.POST.get("q")
                currentFilter = request.POST.get("filter")
                context['query'] = searchString
                context['selected'] = currentFilter
                if searchString:
                    # search for posts WHERE title LIKE '%[searchString]%'
                    if currentFilter == "title":
                        posts = Post.objects.all().filter(title__contains=searchString) 
                    # search for posts WHERE description LIKE '%[searchString]%'
                    elif currentFilter == "description":
                        posts = Post.objects.all().filter(description__contains=searchString)
        
        elif searchType == "Date Posted":
            context['showDateRange'] = True
            context['showSearchBar'] = False
            currentDate = datetime.date.today()
            launchDate = currentDate - datetime.timedelta(7)    # one week ago
            context['currentDate'] = str(currentDate)   # "YYYY-MM-DD"
            context['launchDate'] = str(launchDate)

            searchButtonClicked = request.POST.get("Search")
            if searchButtonClicked:
                context['dateFrom'] = request.POST.get("datefrom")
                context['dateTo'] = request.POST.get("dateto")
                if request.POST.get("datefrom") and request.POST.get("dateto"):
                    dateFrom = datetime.date.fromisoformat(request.POST.get("datefrom"))
                    dateTo = datetime.date.fromisoformat(request.POST.get("dateto"))
            
                    # get number of days
                    #dateRange = datetime.timedelta(dateTo.day-dateFrom.day).days
            
                    # get all posts in the specified range
                    posts = Post.objects.all().filter(date_posted__range=(dateFrom, dateTo))
                    for post in posts:
                        post.date_posted = str(post.date_posted)
            
        # print results for debugging
        for post in posts:
            print("Title: " + post.title,
                  "Description: " + post.description,
                  "Date Posted: " + str(post.date_posted))
    else:
        context['showSearchBar'] = False
        context['showDateRange'] = False
    
    context['searchType'] = searchType
    context['searchButtonClicked'] = searchButtonClicked
    context['posts'] = posts

    print("context = {")
    for key, value in context.items():
        print(" " * 4 + key + ": " + str(value))
    print("}")

    return render(request, "posts/search_posts.html", context)
