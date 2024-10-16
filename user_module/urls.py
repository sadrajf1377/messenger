from django.urls import path

from .views import filter_with_usernames,edit_user_info,Ask_For_Password_Reset,Reset_Password,Ask_For_User_Deletion,Delete_User
urlpatterns=[path('filter_users/<inp>',filter_with_usernames.as_view(),name='filter_users')
             ,path('edit_user_info/',edit_user_info.as_view(),name='edit_user_info')
,path('ask_for_pass_reset/',Ask_For_Password_Reset.as_view(),name='ask_for_pass_reset')
,path('reset_password/<code>',Reset_Password.as_view(),name='reset_password'),
             path('ask_for_user_deletion',Ask_For_User_Deletion.as_view(),name='ask_for_user_deletion'),
path('delete_user',Delete_User.as_view(),name='delete_user')
             ]