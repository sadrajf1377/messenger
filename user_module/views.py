from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView

from .models import cutsom_user
from utils.send_emails import send_email_to
from .forms import Reset_Password_Form
# Create your views here.
class filter_with_usernames(View):
    def get(self,request):
        user_name=request.GET.get('username')
        users=[x['username'] for x in list(cutsom_user.objects.filter(username__contains=user_name).values('username'))]
        print(users)
        return JsonResponse({'users':users})

class Log_Out(View):
    def get(self,request):
        logout(request=request)
        return redirect(reverse('show-chat-groups'))


class edit_user_info(UpdateView):
    model = cutsom_user
    fields = ['username','first_name','last_name','email']
    template_name = 'edit_user_info.html'
    success_url = reverse_lazy('show-chat-groups')
    context_object_name = 'form'
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

class Ask_For_User_Deletion(View):
    def post(self,request):
        try:
            code=get_random_string(length=16)

            res=send_email_to(template_name='delete_user_email.html',to=request.user.email,subject='delete account',contex={'code':code})
            if res>0:
                user: cutsom_user = request.user
                user.delete_code = code
                user.save()
                status='succeed'
            else:
                status='failure'
        except:
            status = 'failure'
        return JsonResponse({'status':status})

@method_decorator(login_required,name='dispatch')
class Delete_User(View):
    def post(self,request):
        print('salam')
        try:
            code=request.POST.get('delete_code')
            user:cutsom_user=request.user

            if user.delete_code == code:
                user.delete()
                status = 'succeed'
            else:
                status='failure'
        except Exception as e:
            status='failure'
        return JsonResponse({'status':status})

class Ask_For_Password_Reset(View):
    def get(self,request):
        return render(request,'ask_password_reset.html')
    def post(self,request):
        try:
          succeed:bool=False
          error:str=''

          code=get_random_string(length=70)
          creds=request.POST.get('email_username')
          user=cutsom_user.objects.get(Q(username=creds)|Q(email=creds))

          email_status=send_email_to(template_name='pass_reset_email.html',to=user.email,subject='reset your password',contex={'code':code})
          if email_status >0:
            user.pass_reset_code = code
            user.save()
            succeed=True
          else:
              error='couldnt send email'
        except Exception as e:
            print(e)
            error='user not found'
        response=render(request,'dynamic_message.html' if succeed else 'ask_password_reset.html',context={'error':error} if not succeed else
        {'message':'to reset your password please visit your email'})
        return response


class Reset_Password(View):
    def get(self,request,code):
        return render(request,'reset_password.html',context={'reset_code':code,'form':Reset_Password_Form()})
    def post(self,request,code):
        reset_code=request.POST.get('reset_code')
        print(reset_code,'hgfhg')
        frm = Reset_Password_Form(request.POST)
        user=cutsom_user.objects.get(pass_reset_code=reset_code)

        if frm.is_valid():
                user.set_password(frm.cleaned_data.get('password'))
                user.pass_reset_code=''
                user.save()
                response=render(request,'dynamic_message.html',context={'message':'accounts password changed successfully'})
        else:
                response = render(request, 'reset_password.html', context={'form': frm,'reset_code':reset_code})
        print(frm.errors)
        return response


