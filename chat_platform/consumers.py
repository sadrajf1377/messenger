# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpRequest
from django.utils.decorators import method_decorator

from groups_and_messages.models import chat_messages
from user_module.models import cutsom_user
from groups_and_messages.models import chat_group
from user_module.models import cutsom_user
online_users={}

class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        my_dict=text_data_json['my_dict']
        destination=my_dict['destination']
        # Send message to room group
        if destination =='group':
         async_to_sync(self.channel_layer.group_send)(
             self.room_group_name,my_dict
         )
        elif destination=='self':
           async_to_sync (self.channel_layer.send)(self.channel_name,my_dict)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username=event["username"]
        my_url=event["avatar_url"]
        print(my_url)
        file_url=event['file_url']
        print('username for recieved message is',event['username'])

        # Send message to WebSocket
        self.send(text_data=json.dumps({"function":"add_message", "message": message,"username":username,"url":my_url,'file_url':file_url,'message_id'
        :event['message_id']}))
    def delete_message(self,event):
        group_id=event['group_id']
        message_id=event['message_id']
        chat_group.objects.filter(id=group_id).first().chat_messages_set.filter(id=message_id).delete()
        old_new=event['old_new']
        self.send(text_data=json.dumps({"function":"delete_message",'group_id':group_id,'message_id':message_id,'old_new':old_new}))
    def send_single_message(self,event):
        layer=online_users[event['username']]
        message=event['message']
        self.send()
    def leave_group(self,event):
        gr_id = event['group_id']
        user_id = self.scope['user'].id

        group = chat_group.objects.get(id=gr_id,group_type=event['group_type'])
        message=f'{self.scope["user"].username} left the chat!'
        chat_messages.objects.create(message=message,group_id=gr_id,m_type=chat_messages.message_types[0][0],user_id=
                                     self.scope['user'].id).save()
        group.users.remove(user_id)
        group.save()
        async_to_sync(
            self.channel_layer.group_send
        )(self.room_group_name,{'type':'announce','message':message,'destination':'group','an_type':'leave',
                                'sent_by':self.scope['user'].username})
    def announce_joining(self,event):
        mes=chat_messages(m_type='aanoucement',message=f'{self.scope["user"].username} joined the chat',user_id=self.scope["user"].id,
                          group_id=event['group_id'])
        mes.save()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{'type':'announce','message':f'{self.scope["user"].username}'
                                                                                                       f'joined the chat','an_type':'join','an_type':'join'})


    def announce(self,event):
        message=event['message']
        if event['an_type'] == 'leave' and event['sent_by'] == self.scope['user'].username:
            return
        self.send(text_data=json.dumps({'function':'announce','message':message}))



#online users dictionary is defined above,this are temp messages,that's why we dont save them in database
#dispatch check all of the functions inside the class

class user_private_consumer(WebsocketConsumer):
    def connect(self):
        online_users[self.scope['user'].username] = self.channel_name
        print(self.scope['user'].username,online_users)
        self.accept()
    def disconnect(self, close_code):
        print('online users are',online_users)
        del online_users[self.scope['user'].username]
        self.accept()
    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        func_type=text_data_json['function_type']
        func=self.__getattribute__(func_type)
        func(text_data_json)
    def create_group(self,event):
        try:
                group_name = event['group_name']
                new_group = chat_group(title=group_name,group_type=event['group_type'])
                new_group.save()
                group_type = event['group_type']
                usnames = event['usernames']
                usnames.append(self.scope['user'].username)
                users = cutsom_user.objects.filter(username__in=usnames).all()

                group_id=new_group.id

                for user in users:
                   if user.username in online_users:
                      async_to_sync(self.channel_layer.send)(online_users[user.username],({'type':'add_to_group','group_name':group_name,'group_id':group_id,
                                                                                      'group_type':group_type}))
                   new_group.users.add(user)
                new_group.save()
                message='group created successfully'

        except Exception as e:

                message='couldnt create this group'
        async_to_sync(self.channel_layer.send)(self.channel_name,({'type': 'alert_user', 'message': message}))

    def alert_user(self,event):
        self.send(text_data=json.dumps({'function_type':'alert','message':event['message']}))
    def add_to_group(self,event):

        self.send(text_data=json.dumps({'function_type':'add_to_group','group_name':event['group_name'],'group_id':event['group_id']
                                           ,'group_type':event['group_type']}))
    def talk_to_a_user(self,event):
        usname=event['target_username']

        async_to_sync(self.channel_layer.send)(online_users[usname],{'type':'recive_from_users','message':event['message']})
    def recive_from_users(self,event):

        self.send(text_data=json.dumps({'function_type':'recieve_message','message':event['message']}))

    def saw_message(self,event):
        if event['target'] in online_users:
          async_to_sync(self.channel_layer.send)(online_users[event['target']],
          {'type':'change_message_status','m_id':event['m_id'],'g_id':event['g_id']})
    def change_message_status(self,event):

        self.send(text_data=json.dumps({'function_type':'change_message_status','data':event}))



