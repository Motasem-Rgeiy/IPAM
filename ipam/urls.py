from django.urls import path
from . import views

urlpatterns = [
  path('' , views.NetworkListView.as_view() , name='network_list'),
  path('network/create/' , views.NetworkCreateView.as_view() , name='network_create'),
  path('network/update/<int:pk>/' , views.NetworkUpdateView.as_view() , name='network_update'),
  path('network/delete/<int:pk>/' , views.NetworkDeleteView.as_view() , name='network_delete'),
  path('network/ips/' , views.IPAddressListView.as_view() , name='ip_list'),
   path('network/ip/update/<int:pk>/' , views.IPAddressUpdateForm.as_view() , name='ip_update'),
  path('network/ip/delete/<int:pk>/' , views.IPAddressDeleteView.as_view() , name='ip_delete'),
  path('network/dashboard' , views.dashboard , name='dashboard'),
  path('ip/assign/<int:pk>/' , views.IPAddressAssignView.as_view() , name='ip_assign')
]
