from django.urls import path
from .views import post_list, post_create, post_edit, post_delete, search2,  post_detail,post_mine

urlpatterns = [
    path('',post_list),
    path('create/',post_create),
    path('edit/<id>/',post_edit.as_view()),
    path('delete/<id>/',post_delete.as_view()),
    path('search/',search2, name="search"),
    path('mine/',post_mine),
    path('<id>/',post_detail),

    
]
