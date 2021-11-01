from django.contrib.auth import login
from django.shortcuts import render
from .models import Post
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView, FormView,CreateView,UpdateView
from .forms import PostEditForm,PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#Get all posts
@login_required
def post_list(request):
    posts = Post.objects.all()
    context = {'post_list':posts}
    return render(request,"posts/post_list.html",context)

#Get specific info for post
@login_required
def post_detail(request,id):
    post = Post.objects.get(id= id)
    context = {
        'post_detail' : post
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

#Post Create View
class post_create(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'post_create_form.html'
    fields = '__all__'
    raise_exception = True
    permission_denied_message = "You are not allowed here!"
    success_url="/posts"

    def handle_no_permission(self):
        return HttpResponseRedirect("/users/login/")
    #def get_object(self,queryset=None):
    #    obj = Post.objects.get(id=self.kwargs['id'])
    #    return obj

#Search for posts
@login_required
def search_posts(request):
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

    context["query"] = searchString
    context["selected"] = currentFilter
    context["searchButtonClicked"] = searchButtonClicked
    context["posts"] = posts
    response = render(request, "posts/search_posts.html", context)
    return response
