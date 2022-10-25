from django.shortcuts import render

#MODELS
from vendor.models import (
    Vendor
)
from menu.models import (
    Category,
    FoodItem
)
# Create your views here.

def market_place(request):
    vendors = Vendor.objects.all().order_by('-created_at')
    vendors_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count': vendors_count
    }
    return render(request, 'marketplace/listings.html',context)

def vendor_detail(request, vendor_slug=None):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)    
    categories = Category.objects.filter(vendor=vendor)
    
    context = {
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'marketplace/vendor_detail.html', context)
