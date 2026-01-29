from django.shortcuts import render , get_object_or_404
from django.views.generic import CreateView ,ListView , UpdateView , DeleteView
from . import models , forms
from django.urls import reverse_lazy , reverse
import ipaddress
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    #Using related_object
    subnets = models.Network.objects.count()
    ips = models.IPAddress.objects.count()
    if not ips:
         used_ips_percentage = 0
         free_ips_percentage = 0
    else:
        used_ips = models.IPAddress.objects.filter(status=1).count()
        free_ips = models.IPAddress.objects.filter(status=2).count()
        used_ips_percentage = used_ips / ips * 100
        free_ips_percentage= free_ips / ips * 100

    recent_activate_ips = models.IPAddress.objects.order_by('-updated_at')[:5]
     
    data = {'subnets':subnets , "ips":ips , "used_ips":used_ips_percentage ,'free_ips':free_ips_percentage , 'recent':recent_activate_ips}
    return render(request , 'network/dashboard.html' , {'data':data})


class NetworkListView(LoginRequiredMixin , ListView):
    model = models.Network
    template_name = 'network/list.html'
   



   # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['total_nets'] = models.Network.objects.count()
    #    return context

class NetworkCreateView(LoginRequiredMixin,CreateView):
    model = models.Network
    form_class = forms.NetowrkCreateForm
    template_name = 'network/create.html'
    success_url = reverse_lazy('network_list')

   # def  form_valid(self, form):
    #    form.instance.user = self.request.user
     #   return super().form_valid(form)
    

class NetworkUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Network
    form_class = forms.NetowrkUpdateForm
    template_name = 'network/update.html'
    def form_valid(self, form):
        
        try:
            count = int(self.request.POST.get('nums' , ''))
        except ValueError:
            count = 0
        net_obj = self.get_object().network_address
        prefix_obj = form.cleaned_data.get('prefix')
        current_net = ipaddress.ip_network(f"{net_obj}/{prefix_obj}" , strict=False)
        #Check overlap
        exist_networks = models.Network.objects.all()
        for net in exist_networks:
            net = ipaddress.ip_network(f"{net.network_address}/{net.prefix}")
            if net.network_address != current_net.network_address:
                if current_net.overlaps(net):
                    form.add_error('prefix' , 'this will cause an overlaps!')
                    return self.form_invalid(form)
        #Prevent update subnet length in case new subnet can not has more than existing hosts  
        count_DB_ips = models.IPAddress.objects.filter(network = self.get_object()).count()
        count_updated_ips = len(list(current_net.hosts()))
        if count_DB_ips > count_updated_ips:
            form.add_error('prefix' , 'This subnet has more than updated prefix can has!')
            return self.form_invalid(form)
            
        instance = form.save()
        target_ips = [str(ipaddress.ip_address(ip)) for ip in current_net.hosts()]
        generated_ips = []

        for host in target_ips:
                if count == 0:
                    break
                is_exist = models.IPAddress.objects.filter(ip_address__contains=host)
                if is_exist:
                    continue
                generated_ips.append(models.IPAddress(ip_address=host , network=instance))
                count-=1
        models.IPAddress.objects.bulk_create(generated_ips)
        
        return super().form_valid(form)
        
                

    def get_success_url(self):
        return reverse('network_update' , args=[self.object.id])
    
class NetworkDeleteView(LoginRequiredMixin,DeleteView):
    model =models.Network
    template_name = 'network/delete.html'
    success_url = reverse_lazy('network_list')




class IPAddressListView(LoginRequiredMixin,ListView):
    model = models.IPAddress
    template_name = 'ip/list_ip.html'
    paginate_by = 5
    context_object_name = 'ips'

 
class IPAddressUpdateForm(LoginRequiredMixin,UpdateView):
    model = models.IPAddress
    form_class = forms.IPAddressUpdateForm
    template_name = 'ip/update.html'
    def get_success_url(self):
        return reverse('ip_update' , args=[self.object.id])
    
    def form_valid(self , form):
        status = form.cleaned_data['status']
        if status == 2:
            form.instance.user = None
        return super().form_valid(form)



class IPAddressDeleteView(LoginRequiredMixin,DeleteView):
    model = models.IPAddress
    template_name = 'ip/delete.html'

    def get_success_url(self):
        return reverse('network_update' ,args=[self.object.network.id])
    


class IPAddressAssignView(UpdateView):
    model = models.IPAddress
    fields = []
    template_name = 'ip/assign_confirmation.html'
    
    def get_success_url(self):
        return reverse('network_update' , args=[self.object.network.id])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 1
        return super().form_valid(form)
    




    


