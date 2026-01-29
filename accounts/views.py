from django.shortcuts import render
from accounts.forms import UserRegisterForm , ProfileForm
from django.views.generic import CreateView , UpdateView
from django.urls import reverse_lazy , reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('network_list')

class ProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    #solve the problem: don't include the id in the urls.py , this function determine it automatically
    def get_object(self, queryset=None):
        return self.request.user
    
 
    
