from django.db import models
from django.contrib.auth.models import User
import ipaddress
from django.core.exceptions import ValidationError
# Create your models here.


PREFIX_CHOICES = [(i, f'/{i}') for i in range(8, 31)]

class Network(models.Model):
    name = models.CharField()
    network_address = models.GenericIPAddressField(protocol='IPv4' , unique=True)
    prefix = models.PositiveSmallIntegerField(choices=PREFIX_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    def clean(self):
        new_network = self.network_address
        new_prefix =  self.prefix
        if new_network and new_prefix:
            try:
                new_net = ipaddress.ip_network(f"{new_network}/{new_prefix}")
                for exist_net in Network.objects.all():
                    exist_net = ipaddress.ip_network(f"{exist_net.network_address}/{exist_net.prefix}" ,strict=False)
                    if exist_net != new_net:
                        if new_net.overlaps(exist_net):
                            raise ValidationError(f'This network is overlaped with {exist_net}')
            except ValueError:
                raise ValidationError('Invalid Network address')
  
       
        


class iPStatus(models.IntegerChoices):
    USED = 1 , 'used'
    FREE = 2 , 'free'

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4' , unique=True)
    status = models.IntegerField(choices=iPStatus.choices , default=iPStatus.FREE)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
    description = models.TextField(blank=True)
    network = models.ForeignKey(Network , on_delete=models.CASCADE , related_name='ip_addresses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

