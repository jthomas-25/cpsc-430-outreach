from django.shortcuts import render
from users.models import CustomUser

# Create your views here.
def home(request):
    user = None
    if request.session.get('email') != None:
        user = CustomUser.objects.get(email=request.session.get('email'))
        return render(request,"home/home_view.html",{'user':user})
    return render(request,'home_view.html')
