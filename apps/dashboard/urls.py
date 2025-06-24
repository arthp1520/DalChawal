from django.urls import path
# from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign_in'),
    path('', views.sign_up, name='sign_up'),
    path('index/', views.index, name='index'),
    path('profile/<int:user_id>/', views.public_profile, name='public_profile'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('show/', views.show, name='show'),
    path('insert/', views.insert, name='insert'),
    path('update-document/<int:doc_id>', views.update_document, name='update_document'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('email_verify/', views.email_verify, name='email_verify'),
    path('explore/', views.explore, name='explore'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('logout/',views.logout,name='logout'),
    

]
