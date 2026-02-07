from django.contrib import admin
from ipam import models
from django.db.models import Count
# Register your models here.

@admin.register(models.Network)
class NetworkAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['name','network_address' , 'prefix' , 'description' , 'created_at' , 'updated_at' , 'ip_address_count']
    list_editable = ['prefix']
    
    def ip_address_count(self , obj):
        return obj.ip_address_count
    def get_queryset(self, request):
        query = super().get_queryset(request)
        query = query.annotate(ip_address_count=Count('ip_addresses'))
        return query
    

@admin.register(models.IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['ip_address' , 'status' , 'user' , 'description' ,'network']
    list_editable = ['status']
  
    

    
    