from django.urls import path
from .views import user_create, user_login, user_edit,user_logout

urlpatterns = [
    path('create/',user_create),
    path('edit/<id>',user_edit),
    path('login/',user_login.as_view()),
    path('logout/',user_logout),
]