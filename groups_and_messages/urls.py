from django.urls import path
from .views import show_chat_groups
from .views import recive_message,Join_Gruop,Search_Groups_Users,Get_Groups_Messages,Mark_Message_As_Seen
urlpatterns=[
 path('',show_chat_groups.as_view(),name='show-chat-groups')
 ,path('receive_messages',recive_message.as_view(),name='receive_messages')
 , path('join/<title>', Join_Gruop.as_view(), name='join_group')
 , path('search_groups_users/<title>', Search_Groups_Users.as_view(), name='search_groups_users')
, path('get_group_messages/<id>/<start>', Get_Groups_Messages.as_view(), name='get_group_messages')
, path('mark_as_seen', Mark_Message_As_Seen.as_view(), name='mark_message_as_seen')
]