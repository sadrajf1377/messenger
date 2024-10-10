from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView
from user_module.forms import Register_form,Login_form,my_form
from user_module.models import cutsom_user
from utils.send_emails import send_email_to
# Create your views here.
#do you think this a good login view,or do i use django's model form to get info from user
class login_user(View):
    def get(self,request):
        form=my_form()
        return render(request,'Login_page.html',context={'form':form})
    def post(self,request):
       form=my_form(request.POST)
       if form.is_valid():
           username_or_email=form.cleaned_data.get('username')
           users=cutsom_user.objects.filter(Q(email=username_or_email)|Q(username=username_or_email))
           if any(users):
               check_password=users.first().check_password(form.cleaned_data.get('password'))
               if check_password:
                   login(request,users.first())
                   q_url=request.POST.get('q_url')
                   if q_url!='':
                       return redirect(q_url)
                   return redirect(reverse('show-chat-groups'))
           form.add_error('password','users with such information not found!Try again')

           return render(request,'Login_page.html',context={'form':form})
       else:
           return render(request, 'Login_page.html', context={'form': form})
class Create_user(View):
    def get(self,request):
        form=Register_form()
        return render(request,'Create_user.html',{'form':form})
    def post(self,request):
        form=Register_form(request.POST,request.FILES)

        if form.is_valid():
                obj:cutsom_user=form.save(commit=False)
                obj.acivation_code = get_random_string(72)
                #we use the django's send email to send email and check if the email was sent succesfully
                email_is_valid=send_email_to(template_name='activate_account.html',subject='Activate your account',to=obj.email,contex={'user_name':obj.username
                                                                                                                      ,'activation_code':obj.acivation_code})>0
                if email_is_valid:
                  obj.set_password(form.cleaned_data.get('password'))
                  obj.save()
                  response=render(request,'dynamic_content.html',{'content':'Check the link we sent to your email to activate your account'})
                else:
                    form.add_error('email','couldnt find such email')
                    response = render(request, 'Create_user.html', {'form': form})
        else:
            response=render(request,'Create_user.html',{'form':form})

        return response




class activate_user(View):
    def post(self,request):
        pass
    def get(self,request,code):
        user=cutsom_user.objects.get(acivation_code=code)
        user.is_active=True
        user.save()

        return render(request,'dynamic_content.html',{'content':'Congratulation!Your Account has been Activated!'})







