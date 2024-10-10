from django.contrib import admin
from .models import chat_group,chat_messages,seen_list
# Register your models here.

class chat_groups_display(admin.ModelAdmin):
    list_display = ['id','title']
    list_display_links = ['title']
    list_per_page = 12

class chat_message_display(admin.ModelAdmin):
    list_display = ['__str__','group','user']

class seen_list_settings(admin.ModelAdmin):
     list_display = ['message']


admin.site.register(chat_group,chat_groups_display)
admin.site.register(chat_messages,chat_message_display)
admin.site.register(seen_list,seen_list_settings)
#admin.site.register(Who_Seen_This_Message)