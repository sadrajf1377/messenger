from django.urls import path
from .views import login_user,Create_user,activate_user
urlpatterns=[path('',login_user.as_view(),name='login')
             ,path('create_user',Create_user.as_view(),name='create_user')
             ,path('activate_user/<code>',activate_user.as_view(),name='activate_user')]