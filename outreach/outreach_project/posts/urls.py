from django.urls import path
from .views import post_list, post_create, post_edit, post_delete, search_posts, post_detail

urlpatterns = [
    path('',post_list),
    path('create/',post_create.as_view()),
    path('edit/<id>/',post_edit.as_view()),
    path('delete/<id>/',post_delete.as_view()),
    path('search/',search_posts),
    path('<id>/',post_detail),
    
]
