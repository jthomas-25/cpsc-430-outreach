from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import Post
from users.models import CustomUser
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView, FormView, CreateView, UpdateView
from .forms import PostEditForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#Get all posts
@login_required
def post_list(request):
    posts = Post.objects.all()
    user = CustomUser.objects.get(email=request.session.get('email'))
    context = {
        'post_list' : posts,
        'user' : user
    }
    return render(request,"posts/post_list.html",context)

@login_required
def post_mine(request):
    user = CustomUser.objects.get(email=request.session['email'])
    posts = user.posts.all()
    context = {'post_list':posts,'user':user}
    return render(request,'posts/post_mine.html',context)

#Get specific info for post
@login_required
def post_detail(request,id):
    post = Post.objects.get(id=id)
    user = CustomUser.objects.get(email=request.session.get('email'))
    
    if request.method == "POST":
        if user.is_employer or user.is_admin:
            editPostButtonClicked = request.POST.get("Edit Post")
            deletePostButtonClicked = request.POST.get("Delete Post")
            if editPostButtonClicked:
                return HttpResponseRedirect("/posts/edit/" + str(post.id))
            elif deletePostButtonClicked:
                return HttpResponseRedirect("/posts/delete/" + str(post.id))

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
                return HttpResponseRedirect("/")
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
class post_delete(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'post_confirm_delete.html'
    raise_exception = True
    permission_denied_message = "You are not allowed here!"

    def get_object(self,queryset=None):
        obj = Post.objects.get(id=self.kwargs['id'])
        return obj
    def handle_no_permission(self):
        return HttpResponseRedirect("/users/login/")

#Post Edit View
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
        return HttpResponseRedirect("/users/login/")


@login_required
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

#Search for posts
@login_required
def search_posts(request):
    posts = []
    searchString = ""
    searchButtonClicked = ""
    currentFilter = ""

    if request.method == "POST":
        searchString = request.POST.get("q", "")
        searchButtonClicked = request.POST.get("Search", "")
        currentFilter = request.POST.get("filter", "")
        if searchString:
            #request.session["search_filter"] = currentFilter
            # search for posts WHERE title LIKE '%[searchString]%'
            if currentFilter == "title":
                posts = Post.objects.all().filter(title__contains=searchString) 
            # search for posts WHERE description LIKE '%[searchString]%'
            elif currentFilter == "description":
                posts = Post.objects.all().filter(description__contains=searchString)
            for post in posts:
                print("Title: " + post.title,
                      "Description: " + post.description)
    
    context = {
        'query' : searchString,
        'selected' : currentFilter,
        'searchButtonClicked' : searchButtonClicked,
        'posts' : posts
    }
    """
    context["query"] = searchString
    context["selected"] = currentFilter
    context["searchButtonClicked"] = searchButtonClicked
    context["posts"] = posts
    """
    return render(request, "posts/search_posts.html", context)
