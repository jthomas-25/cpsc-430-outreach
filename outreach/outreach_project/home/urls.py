from django.urls import path
from .views import home, admin_portal 

urlpatterns = [
    path('',home),
    path('admin_portal/',admin_portal),
]
