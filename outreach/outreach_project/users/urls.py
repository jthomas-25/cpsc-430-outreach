from django.urls import path, include
from .views import change_password,contact_user, user_list, user_create, user_edit, user_login, user_logout, user_detail,user_profile, account_delete
from django.contrib import admin
from django_email_verification import urls as email_urls

urlpatterns = [
    path('',user_list),
    #path('admin/', admin.site.urls),
    path('create/',user_create),
    path('edit/<id>',user_edit),
    path('login/',user_login.as_view()),
    path('logout/',user_logout),
    path('view/',user_detail),
    path('myprofile/',user_profile),
    path('verification/', include('verify_email.urls')),
    path('email/', include(email_urls)),
    path('myprofile/delete/',account_delete),
    path('contact/<id>',contact_user),
    path('changePassword/',change_password)
    #path('<id>/',user_detail),

]
