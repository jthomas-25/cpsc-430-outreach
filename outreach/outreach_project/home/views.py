from django.shortcuts import render
from users.models import CustomUser

# Create your views here.
def home(request):
    user = None
    if request.session.get('email') != None:
        user = CustomUser.objects.get(id=request.session.get('user_id'))
        return render(request,"home/home_view.html",{'user':user})
    return render(request,'home_view.html')
