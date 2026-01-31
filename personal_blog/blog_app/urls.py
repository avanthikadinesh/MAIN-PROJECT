"""
URL configuration for personal_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('blog/', blog_list, name='blog_list'),
    path('blog/add/', add_post, name='add_post'),  
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', post_list, name='post_list'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('blog/', views.blog_list, name='blog_list'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('author/<str:username>/', views.author_profile, name='author_profile'),
    path('follow/<str:username>/', views.follow_author, name='follow_author'),
    path('unfollow/<str:username>/', views.unfollow_author, name='unfollow_author'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('author/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('author/<str:username>/following/', views.following_list, name='following_list'),
    path('save/<int:post_id>/', views.toggle_save_post, name='toggle_save_post'),
    path('saved-posts/', views.saved_posts, name='saved_posts'),
    path('notifications/', views.notifications_view, name='notifications'),

]









