from django.shortcuts import render
from user_module.forms import my_form

def Quened_Request(func):
    def To_do(*args,**kwargs):
        req=args[0]
        print(func)
        if req.user.is_authenticated:
           return func(*args,**kwargs)
        else:
            abs_url=req.build_absolute_uri()
            return render(req,'Login_page.html',{'quened_url':abs_url,'form':my_form(None)})
    return To_do

