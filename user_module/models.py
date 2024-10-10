from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models




def password_validator(password:str):
    special_chars=['_','-','@','/']
    numbers=str(list(range(0,10,1)))
    sp_and_number=any([x for x in password if x in numbers]) and any([x for x in password if x in special_chars])
    is_upper=not password.islower()
    correct_lentgh=len(password)>=8 and len(password)<=16
    return is_upper and sp_and_number and correct_lentgh
# Create your models here.
class cutsom_user(AbstractUser):

    acivation_code=models.CharField(max_length=72,verbose_name='user activation code',default='')
    avatar=models.ImageField(upload_to='users_avatars/',null=True,blank=True)
    password = models.CharField(max_length=100,null=False,blank=False)
    is_private=models.BooleanField(default=False,verbose_name='Is User Private')
    pass_reset_code=models.CharField(max_length=70,verbose_name='password reset code',null=False,blank=False)
    delete_code=models.CharField(max_length=16,null=True,blank=True,verbose_name='delete_user code')
    def get_avatar(self):
        try:
            return self.avatar.url
        except:
            return ''
    class Meta:
        verbose_name='custom_user'
        verbose_name_plural='custom_users'
        db_table='custom_user'
    def __str__(self):
        return self.username


