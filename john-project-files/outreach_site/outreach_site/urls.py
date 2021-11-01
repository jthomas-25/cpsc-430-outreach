"""outreach_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from job_board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('job_board/admin/home/', views.adminHome, name='admin-home'),
    #path('job_board/admin/manage-posts/', views.adminManagePosts, name='admin-manage-posts'),
    path('job_board/admin/manage-accounts/', views.adminManageAccounts, name='admin-manage-accounts'),
    path('job_board/admin/view-account/', views.adminViewAccount, name='admin-view-account'),
    path('', views.index, name='index'),
    path('job_board/', views.index, name='main-page'),
    path('job_board/login-type/', views.loginType, name='login-type'),
    path('job_board/login/', views.login, name='login'),
    path('job_board/login/login-success/', views.loginSuccess, name='login-success'),
    path('job_board/logout/', views.logout, name='logout'),
    path('job_board/student/home/', views.studentHome, name='student-home'),
    path('job_board/student/search-posts/', views.searchPosts, name='search-posts'),
    path('job_board/student/view-post/', views.viewPost, name='view-post'),
    path('job_board/employer/home/', views.employerHome, name='employer-home'),
    path('job_board/employer/create-post/', views.employerCreatePost, name='employer-create-post'),
    path('job_board/employer/create-post/post-submitted/', views.postSubmitted, name='post-submitted'),
    path('job_board/employer/view-posts/', views.employerViewPosts, name='employer-view-posts'),
    path('job_board/employer/view-post/', views.viewPost, name='view-post'),
]
