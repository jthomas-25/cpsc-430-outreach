from django.shortcuts import render
from posts.models import Post
from users.models import CustomUser

# Create your views here.
def home(request):
    user = None
    if request.session.get('email') != None:
        user = CustomUser.objects.get(id=request.session.get('user_id'))
        # list all currently available jobs for convenient access
        posts = Post.objects.all()
        posts = posts.exclude(status="pending")
        for post in posts:
            post.date_posted_str = post.get_date_str(post.date_posted)
        context = {
            'user': user,
            'post_list': posts
        }
        return render(request, "home/home_view.html", context)
    return render(request,'home_view.html')

def admin_portal(request):
    posts = Post.objects.filter(status="pending")
    users = CustomUser.objects.filter(is_pending=True)
    context = {'posts':posts,'users':users}
    return render(request,'admin_portal_view.html',context)

