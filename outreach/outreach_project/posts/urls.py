from django.urls import path
from .views import post_list, post_create, post_edit, post_delete, search2,  post_detail,post_mine

app_name = 'posts'
urlpatterns = [
    path('',post_list,name='list'),
    path('create/',post_create,name='create'),
    path('edit/<id>/',post_edit.as_view(),name='edit'),
    path('delete/<id>/',post_delete.as_view(),name='delete'),
    path('search/',search2,name='search'),
    path('mine/',post_mine,name='mine'),
    path('<id>/',post_detail,name='detail'),

]
