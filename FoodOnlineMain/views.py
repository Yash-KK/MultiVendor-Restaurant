from django.shortcuts import render
from django.http import HttpResponse

#MODELS
from vendor.models import (
    Vendor
)

#create your views here
def home(request):
    vendors = Vendor.objects.filter(user__is_active=True, is_approved=True).order_by('created_at')[:8]
    
    context = {
        'vendors':vendors
    }
    return render(request, 'home.html',context)

