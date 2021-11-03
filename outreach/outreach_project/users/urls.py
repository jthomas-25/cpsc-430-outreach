from django.urls import path
from .views import user_list, user_create, user_edit, user_login, user_logout, user_detail

urlpatterns = [
    path('',user_list),
    path('create/',user_create),
    path('edit/<id>',user_edit),
    path('login/',user_login.as_view()),
    path('logout/',user_logout),
    path('view/',user_detail),
    #path('<id>/',user_detail),

]
