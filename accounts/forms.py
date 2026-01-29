from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm , UserChangeForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm , self).__init__(*args, **kwargs)
    
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password')

class UserRegisterForm(UserCreationForm):
        first_name = forms.CharField(label='First Name')
        last_name = forms.CharField(label='Last Name')
        username = forms.CharField(label='Username')
        email = forms.CharField(label='Email')
        password1 = forms.CharField(label='Password')
        password2 = forms.CharField(label='Password Confirmation')
        class Meta(UserCreationForm.Meta):
             fields = ['first_name' , 'last_name' , 'username' , 'email' ]


class ProfileForm(UserChangeForm):
     password = None
     class Meta:
          model = User
          fields = ['first_name' , 'last_name'  , 'email' ]
          
