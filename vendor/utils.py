#MODELS
from .models import (
    Vendor
)

#helper functions
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None    
    return vendor
