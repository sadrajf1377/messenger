from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string

from user_module.models import cutsom_user
# Create your models here.

class chat_group(models.Model):
    title=models.CharField(max_length=100,verbose_name="group's title",default='',unique=True,error_messages={'unique':'A Group With Such Name Exists!'})
    users=models.ManyToManyField(cutsom_user,verbose_name="group's users")
    picture=models.ImageField(upload_to='groups_images',null=True,blank=True)
    types=(('two','two'),('many','many'))
    group_type=models.CharField(max_length=5,choices=types,default='many',null=False,blank=False,verbose_name='type of group chat')

    def children_sorted_by_date(self,start=0,length=5):
        return self.chat_messages_set.order_by('-creation_date').all()[start:start+length:]
    def save(
        self,*args
    ):

        super().save(*args)


    def __str__(self):

        return self.title


    class Meta:
        db_table='chat_groups'
        verbose_name='chat_group'
        verbose_name_plural='chat_groups'

class chat_messages(models.Model):

    message_types=(('aanoucement','aanoucement'),('message','message'))
    m_type=models.CharField(default='message',max_length=15,verbose_name='message_type',choices=message_types)
    group=models.ForeignKey('chat_group',verbose_name='parent group of message',null=True,blank=True,on_delete=models.CASCADE,db_index=True)
    message=models.CharField(max_length=1000,verbose_name="message's text",default='')
    file=models.FileField(upload_to='group_photos',verbose_name="message's file",null=True,blank=True)
    user=models.ForeignKey(cutsom_user,verbose_name='the use who sent this message',null=True,blank=True,on_delete=models.CASCADE)
    creation_date=models.DateTimeField(verbose_name="message's date",auto_now_add=True)
    def file_url(self):
        try:
            result=self.file.url
        except:
            result='na'
        return result
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        create_list=self.id == None
        super().save()
        if create_list:

            seen_list.objects.create(message_id=self.id).save()




    class Meta:
        db_table='chat_messages'
        verbose_name='chat_message'
        verbose_name_plural='chat_messages'

class seen_list(models.Model):

    message=models.OneToOneField(chat_messages,on_delete=models.CASCADE,verbose_name='the message',null=False)
    users=models.ManyToManyField(cutsom_user,verbose_name='users who saw this message')


