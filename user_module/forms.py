
from django import forms
from .models import cutsom_user,password_validator

class Register_form(forms.ModelForm):

    class Meta:
        model=cutsom_user
        fields= ['username','email','avatar','password']
        labels= {'username':'username','email':'email','password':'password','avatar':'avatar'}
        widgets={'password':forms.PasswordInput()}

    password_repeat = forms.CharField(label='password_repeat', widget=forms.PasswordInput())

    def is_valid(self):
        passwords_match=self.data.get('password')==self.data.get('password_repeat')
        valid_pass=password_validator(self.data.get('password'))
        if not passwords_match:
            print('passwords didnt match')
            self.add_error('password_repeat','passwords dont match')
        if not valid_pass:
            print('passwords not safe')
            self.add_error('password', 'password must contain at least one special character'
                                       'ex:_ , one uppercase word ex:H and one number,also it must contain atleast eight character and less than 16 characters')
        return passwords_match and passwords_match(self.data.get('password'))



class Login_form(forms.ModelForm):

    class Meta:
        model=cutsom_user
        fields=['username','password']
        labels={'username':'username','password':'Password'}
        widgets={'password':forms.PasswordInput(),'username':forms.TextInput(attrs={'placeholder':'enter either your user name or your email'})}
class my_form(forms.Form):
    username=forms.CharField(max_length=20,label='username or email:',widget=forms.TextInput(attrs={'placeholder':'enter your email or username',
                                                                                                    'name':'username','id':'id_username'}))
    password=forms.CharField(max_length=20,label='password',widget=forms.PasswordInput(attrs={'placeholder':'enter your password','id':'id_password'
                                                                                              ,'name':'password'}))

class Reset_Password_Form(forms.Form):
    password=forms.CharField(max_length=8,label='password',widget=forms.PasswordInput(attrs={'required':True}))
    password_repeat=forms.CharField(max_length=8,label='password_repeat',widget=forms.PasswordInput(attrs={'required':True}))
    def is_valid(self):
        print(self.data.get('password'))
        password_match=self.data.get('password') == self.data.get('password_repeat')
        valid_password=password_validator(self.data.get('password'))
        if not password_match:
            self.add_error('password_repeat','passwords didnt match')
        if not valid_password:
            self.add_error('password','password must contain at least one special character'
                              'ex:_ , one uppercase word ex:H and one number,also it must contain atleast eight character and less than 16 characters')
        res=super().is_valid() and password_match and valid_password
        return res

