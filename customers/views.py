from django.shortcuts import render, redirect
from django.contrib import messages
#FORMS
from accounts.forms import (
    UserFormCustomer,
    UserProfileForm
)
#MODELS
from accounts.models import (
    User,
    UserProfile
)
# Create your views here.
def cprofile(request):    
    user = User.objects.get(email=request.user)
    user_profile = UserProfile.objects.get(user=user)
    
    if request.method == 'POST':
        user_form = UserFormCustomer(request.POST,instance=user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Updated the Customer Profile')
            return redirect('cprofile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
                    
    else:
    
        user_form = UserFormCustomer(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
    context = {
        'u_form': user_form,
        'user_profile_form': profile_form,
        
        'user_profile': user_profile
    }
    return render(request, 'customers/cprofile.html', context)


