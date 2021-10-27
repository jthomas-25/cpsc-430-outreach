from django.urls import path
from .views import post_create, post_delete, post_list,post_detail,post_edit

urlpatterns = [
    path('',post_list),
    path('create/',post_create.as_view()),
    path('edit/<id>/',post_edit.as_view()),
    path('delete/<id>/',post_delete.as_view()),
    path('<id>/',post_detail),
    
]