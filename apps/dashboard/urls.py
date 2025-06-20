# # from django.urls import path
# # from .views import *

# # urlpatterns = [
# #     path('', 'view.index'),
# # # ]

# # from django.urls import path
# # from . import views
# # # from .views import *

# # urlpatterns = [
# #     path('', views.insert,name='insert'),  #  Call the index view function
# #     path('show/', views.show,name='show'),  #  Call the index view function
# # ]

# from django.urls import path
# # from .views import *
# from . import views

# urlpatterns = [
#     # path('', views.sign_in, name='sign_in'),
#     path('sign-in/', views.sign_in, name='sign_in'),
#     path('', views.sign_up, name='sign_up'),
#     path('forgot-password/', views.forgot_password, name='forgot_password'),
#     path('index/', views.index, name='index'),
#     path('show/', views.show, name='show'),
#     path('insert/', views.insert, name='insert'),
#     path('update-post/<int:post_id>', views.update_post, name='update_post'),
#     path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
#     path('profile/', views.profile, name='profile'),
#     path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    

# ]


# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('', 'view.index'),
# # ]

# from django.urls import path
# from . import views
# # from .views import *

# urlpatterns = [
#     path('', views.insert,name='insert'),  #  Call the index view function
#     path('show/', views.show,name='show'),  #  Call the index view function
# ]

from django.urls import path
# from .views import *
from . import views

urlpatterns = [
    # path('', views.sign_in, name='sign_in'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('', views.sign_up, name='sign_up'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('index/', views.index, name='index'),
    path('show/', views.show, name='show'),
    path('insert/', views.insert, name='insert'),
    path('update-post/<int:post_id>', views.update_post, name='update_post'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('email_verify/', views.email_verify, name='email_verify'),
    

]
