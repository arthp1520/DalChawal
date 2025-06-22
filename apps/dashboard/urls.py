from django.urls import path
# from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign_in'),
    path('', views.sign_up, name='sign_up'),
   
    # inbuilt function of python django
    
        path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dashboard/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dashboard/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='dashboard/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='dashboard/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('index/', views.index, name='index'),
    path('profile/<int:user_id>/', views.public_profile, name='public_profile'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('show/', views.show, name='show'),
    path('insert/', views.insert, name='insert'),
    path('update-post/<int:post_id>', views.update_post, name='update_post'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-document/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('email_verify/', views.email_verify, name='email_verify'),
    path('logout/',views.logout,name='logout'),
    

]
