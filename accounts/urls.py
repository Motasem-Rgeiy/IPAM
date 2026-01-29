from django.urls import path , include
from django.contrib.auth.views import LoginView
from accounts.forms import UserLoginForm
from accounts.views import UserRegisterView , ProfileView

urlpatterns = [
    path('login/' ,LoginView.as_view(authentication_form=UserLoginForm)  , name='login'),
    path('register/', UserRegisterView.as_view() , name='register'),
    path('profile/' , ProfileView.as_view() , name='profile')    ,
    path('' , include('django.contrib.auth.urls'))
]
