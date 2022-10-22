from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Helper functions
from .utils import (
    detect_user,  
    send_verification_mail,
    send_reset_password_mail    
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
    user = request.user
    answer = detect_user(user)
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
            
            send_verification_mail(request,user)
            
            messages.success(request, 'A verification Email has been sent')
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
            
            send_verification_mail(request,user)
            
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
            messages.error(request, 'Invalid credentials!')
            return redirect('login-user')      
    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    # Gotta activate the account by setting the is_active to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print(user)
        messages.success(request, 'Congratulation! Your account is activated.')       
        return redirect('login-user') 
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('login-user')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset-password')
    else:
        messages.error(request, 'The link has been expired!')
        return redirect('login-user')
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('login-user')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email__exact=email)
        if user.exists():
            user = list(user)[0]
            print(user.pk)
            # if the user exists, send a reset_password mail to the user
            send_reset_password_mail(request,user)
            messages.success(request, 'Password reset link has been sent to your Email')
            return redirect('login-user')
        else:
            messages.error(request, 'Email does not exist!')
            return redirect('forgot-password')
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']       
       
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password has been set successfully! You can Login now!')
            return redirect('login-user')        
        else:
            messages.error(request, 'Passwords do not Match!')
            return redirect('reset-password')
    
    return render(request, 'accounts/reset_password.html')

@login_required(login_url='login-user')
@user_passes_test(if_customer_user)
def customer_dashboard(request):
    return render(request, 'accounts/cDashboard.html')

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def vendor_dashboard(request):
    return render(request, 'accounts/vDashboard.html')