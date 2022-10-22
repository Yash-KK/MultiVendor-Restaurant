from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Helper functions
from .utils import (
    detect_user,  
    
)

#FORMS
from .forms import (
    UserForm,
    VendorForm
)
#MODELS
from .models import (
    User,
    UserProfile
)

# Create your views here.
def if_customer_user(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
               
def if_vendor_user(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied               

def my_account(request):
    answer = detect_user(request.user)
    return redirect(answer)


def register_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already Logged In!')
        return redirect('my-account')
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
             
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)
            user.set_password(password)
            user.role = User.CUSTOMER            
            user.save()
            messages.success(request, 'User Registered Successfully!')
            return redirect('register-user')
        else:
            print(form.errors)
    else:            
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html',context)

def register_vendor(request):    
    if request.user.is_authenticated:
        messages.info(request, 'You are already Logged In!')
        return redirect('my-account')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
             
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)
            user.set_password(password)
            user.role = User.VENDOR            
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Vendor Registeration completed! Please wait for admin approval.')
            return redirect('register-vendor')            
        else:
            print(form.errors)
            print(v_form.errors)                       
    else:
        form = UserForm()
        v_form = VendorForm()
        
    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request, 'accounts/registerVendor.html', context)



def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already Logged In!')
        return redirect('my-account')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('my-account')
        else:
            messages.error(request, 'Please try again!')
            return redirect('login-user')      
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('login-user')

@login_required(login_url='login-user')
@user_passes_test(if_customer_user)
def customer_dashboard(request):
    return render(request, 'accounts/cDashboard.html')

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def vendor_dashboard(request):
    return render(request, 'accounts/vDashboard.html')