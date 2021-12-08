from django.urls import path
from .views import home, admin_portal 

app_name = 'home'
urlpatterns = [
    path('',home,name='index'),
    path('admin_portal/',admin_portal,name='admin-portal'),
]
