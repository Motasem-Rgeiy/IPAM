from django import forms
from ipam.models import Network , IPAddress
import ipaddress
class NetowrkCreateForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['name' , 'network_address' , 'prefix' , 'description']
        widgets = {
            'name':forms.TextInput(),
            'network_address': forms.TextInput(),
            'prefix':forms.Select(),
            'description':forms.Textarea()
        }

    def clean(self):
        cleaned_data = super().clean()
        new_network = cleaned_data.get('network_address' , '')
        new_prefix =  cleaned_data.get('prefix' , '')
        if new_network and new_prefix:
            try:
                new_net = ipaddress.ip_network(f"{new_network}/{new_prefix}")
                for exist_net in Network.objects.all():
                    exist_net = ipaddress.ip_network(f"{exist_net.network_address}/{exist_net.prefix}" ,strict=False)
                    if new_net.overlaps(exist_net):
                        raise forms.ValidationError(f'This network is overlaped with {exist_net}')
            except ValueError:
                raise forms.ValidationError('Invalid Network address')
       
        
        return cleaned_data
    
attrs = {'class': 'block w-full rounded-md border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2',}
class NetowrkUpdateForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ['name' , 'prefix' , 'description']
        widgets = {
            'name':forms.TextInput(attrs=attrs),
            'prefix':forms.Select(attrs=attrs),
            'description':forms.Textarea(attrs=attrs)
        }

class IPAddressUpdateForm(forms.ModelForm):
    class Meta:
        model = IPAddress
        fields = ['status' , 'description']
        widgets = {
            'status':forms.Select(attrs=attrs),
             'description':forms.Textarea(attrs=attrs),
        }









