from django.urls import path
from .views import user_list, user_create, user_edit, user_login, user_logout, user_detail,user_profile
from django.conf.urls import include
urlpatterns = [
    path('',user_list),
    path('create/',user_create),
    path('edit/<id>',user_edit),
    path('login/',user_login.as_view()),
    path('logout/',user_logout),
    path('view/',user_detail),
    path('myprofile/',user_profile),
    path('verification/', include('verify_email.urls'))	
    #path('<id>/',user_detail),

]
