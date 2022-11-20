from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import simplejson as json

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
from orders.models import (
    Order,
    OrderedFood
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

@login_required(login_url='login-user')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')    
    context = {
        'orders': orders
    }
    return render(request, 'customers/my_orders.html', context)

@login_required(login_url='login-user')
def order_detail(request, id):
    order_detail = Order.objects.get(order_number=id)
    ordered_food = OrderedFood.objects.filter(order=order_detail)
    sub_total = 0 
    for item in ordered_food:
        sub_total += item.amount
    tax_data = json.loads(order_detail.tax_data)
    context = {
        'order': order_detail,
        # 'trans_id': trans_id,
        'ordered_food': ordered_food,
        'tax_data': tax_data,
        
        'sub_total': sub_total
    }
    return render(request, 'customers/order_detail.html', context)
