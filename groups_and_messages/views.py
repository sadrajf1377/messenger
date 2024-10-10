import random

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Case, When, Value, BooleanField, Exists, Q, OuterRef, IntegerField, CharField, \
    F, ExpressionWrapper
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import safe
from django.urls import reverse

import user_module.apps
from utils.decorators import Quened_Request
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views import View
from django.views.generic import ListView
from .models import chat_group
from user_module.models import cutsom_user
# Create your views here.
from utils.send_emails import send_email_to

from groups_and_messages.models import chat_messages
@method_decorator(login_required,name='dispatch')
class show_chat_groups(View):
    def get(self,request:HttpRequest):
     groups=chat_group.objects.\
         filter(users=request.user)
     grs={x.pk:x.chat_messages_set.exclude(user=request.user).exclude(seen_list__users=request.user).all().count() for x in groups}
     titles = {x.pk: x.users.exclude(username=request.user.username).first().username for x in groups if x.group_type=='two'}
     groups = groups.annotate(
         my_title=Case(
             *[When(pk=key, then=Value(value)) for key, value in titles.items()],
             default=Value(''),
             output_field=CharField()
         )
     ).annotate(unread_count=Case(
         *[When(pk=key,then=Value(value)) for key,value in grs.items()],default=0,output_field=IntegerField()))
    
     for obj in groups:
         print(obj,obj.unread_count)
     contex={'groups':groups}
     return render(request,'chat_room_page.html',context=contex)

class recive_message(View):
    def post(self,request:HttpRequest):
        recieved_file=request.FILES.get('message_file') or None #retrives the file  from input named 'message_file' inside that form
        message=request.POST.get('message') #retrives the message from input named 'message' inside that form
        group_id=request.POST.get('group_id')
        new_message=chat_messages(message=message,file=recieved_file,group_id=group_id,user_id=request.user.id)
        new_message.save()
        file_url=new_message.file.url if new_message.file else 'na'
        return JsonResponse({'message':new_message.message,'file_url':file_url ,'message_id':new_message.id})

@method_decorator(Quened_Request,name='dispatch')
class Join_Gruop(View):
    def get(self,request:HttpRequest,title):
        try:
           group=chat_group.objects.get(title=title)
           if not group.users.contains(request.user):
              group.users.add(request.user)
              group.save()
           succeed=True
        except:
            succeed=False
        response=redirect(reverse('show-chat-groups')) if succeed else HttpResponse('Request Could not be satisfied')
        return response

    def post(self,request,title):
        print(title)
        try:
            group = chat_group.objects.get(title=title)
            if not group.users.contains(request.user):
                group.users.add(request.user)
                group.save()
            query_set = group.children_sorted_by_date().annotate(is_seen=Case(When(Q(seen_list__users__isnul=False),then=Value(True)),default=False,
                                                                              output_field=BooleanField()))\
                .annotate(is_read=Case(When(Q(seen_list__users=request.user),then=Value(True)),default=False,output_field=BooleanField()))
            messages = [[x.message, x.user.username, x.file_url(), x.user.avatar.url, x.m_type,x.is_seen,x.is_read,x.id] for x in query_set]
            succeed = True
        except Exception as e:
            print(e.args)
            succeed = False

        response = JsonResponse({'status': 'succeed','group_type':group.group_type if succeed else 'failure', 'messages': messages if succeed else None})
        return response



@method_decorator(login_required,name='dispatch')
class Search_Groups_Users(View):
    def get(self,request,title):
        groups=[['group',x.title,x.id] for x in chat_group.objects.exclude(users=request.user).filter(Q(title__contains=title,group_type='many'))
                ][:12]
        users_query=cutsom_user.objects.filter(username__contains=title).exclude(id=request.user.id).annotate(
            exist=Exists(chat_group.objects.filter(Q(users__username=request.user.username) and Q(users__username=OuterRef('username'))))
        ).exclude(exist=True)[:12]
        users=[['user',x.username] for x in users_query][:12]

        groups.extend(users)
        for us in users_query:
            print(us.username,us.exist)

        print(groups)
        result=JsonResponse({'result':groups})
        return result

class Get_Groups_Messages(View):
    def get(self,request,id,start):
        if not request.user.is_authenticated:
            return HttpResponse('',status=404)
        try:
            group=chat_group.objects.get(id=id,users=request.user)
            messages=group.children_sorted_by_date(start=int(start),length=5).annotate(is_read=Case(When(Q(seen_list__users=request.user),then=Value(True)),default=
                                                                                                    False,output_field=BooleanField())).annotate(
                is_seen=Case(When(Q(seen_list__users__isnull=False),then=Value(True)),default=False,output_field=BooleanField())
            )

            messages=[[x.message,x.user.username,x.user.avatar.url,x.file_url(),x.is_seen,x.is_read,x.id] for x in  messages]
            res={'messages':list(messages),'status':200}
            print(messages,id)

        except Exception as e:
            print(e)
            res={'status':404}
        return JsonResponse(res,status=200 if res!={} else 404)

class Mark_Message_As_Seen(View):
    def post(self,request):
        print('i was called')
        try:
            group_id = request.POST.get('group_id')
            mess=chat_messages.objects.get(group_id=group_id,id=request.POST.get('m_id'),group__users=request.user)
            mess.seen_list.users.add(request.user)
            mess.save()
            status='succeed'
            username=mess.user.username
        except Exception as e:
            print(e)
            status='failure'
            username=''
        return JsonResponse({'status':status,'username':username})