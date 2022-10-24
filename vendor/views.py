from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# VIEWS
from accounts.views import (
    if_vendor_user
)
#FORMS
from accounts.forms import (
    VendorForm,
    UserProfileForm
)

#MODELS
from .models import (
    Vendor
)
from accounts.models import (
    UserProfile
)
 
# Create your views here.
@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def v_profile(request):  
    vendor = Vendor.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES,instance=vendor) 
        user_profile_form = UserProfileForm(request.POST, request.FILES,instance=user_profile)
        if vendor_form.is_valid() and user_profile_form.is_valid():
            vendor_form.save()
            user_profile_form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('v-profile')
        else:
            print(vendor_form.errors)
            print(user_profile_form.errors)
    else:    
        vendor_form = VendorForm(instance=vendor) 
        user_profile_form = UserProfileForm(instance=user_profile)
        
    context = {
        'vendor_form': vendor_form,
        'user_profile_form': user_profile_form,
        
        'vendor':vendor,
        'user_profile':user_profile
    }
    return render(request, 'vendor/v_profile.html', context)


