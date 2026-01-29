from django.db import models
from django.contrib.auth.models import User
# Create your models here.


PREFIX_CHOICES = [(i, f'/{i}') for i in range(8, 31)]

class Network(models.Model):
    name = models.CharField()
    network_address = models.GenericIPAddressField(protocol='IPv4' , unique=True)
    prefix = models.PositiveSmallIntegerField(choices=PREFIX_CHOICES)
    description = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class iPStatus(models.IntegerChoices):
    USED = 1 , 'used'
    FREE = 2 , 'free'

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4' , unique=True)
    status = models.IntegerField(choices=iPStatus.choices , default=iPStatus.FREE)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
    description = models.CharField(null=True)
    network = models.ForeignKey(Network , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

