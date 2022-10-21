from django.shortcuts import redirect, render
from django.contrib import messages
#FORMS
from .forms import (
    UserForm
)
#MODELS
from .models import (
    User
)

# Create your views here.
def register_user(request):
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
