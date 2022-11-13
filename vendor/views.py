from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from django.db import IntegrityError
#UTILS
from .utils import get_vendor
# VIEWS
from accounts.views import (
    if_vendor_user
)
#FORMS
from accounts.forms import (
    VendorForm,
    UserProfileForm
)
from menu.forms import (
    CategoryForm,
    FoodItemForm
)
from .forms import (
    OpeningHourForm
)

#MODELS
from .models import (
    Vendor,
    OpeningHour
)
from accounts.models import (
    UserProfile
)
from menu.models import (
    Category,
    FoodItem
)
 
# Create your views here.
@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def v_profile(request):  
    vendor = get_vendor(request)
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

 
@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    
    context = {
        'categories':categories
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def items_by_category(request, category_slug=None):
    vendor = get_vendor(request)
    category = Category.objects.get(slug=category_slug)
    
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    
    context = {
        'category':category,
        'food_items':food_items
    }
    return render(request, 'vendor/items_by_category.html', context)


@login_required(login_url='login-user')
@user_passes_test(if_vendor_user) 
def add_category(request):    
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            # category.slug = slugify(cat_name) 
            category.save()
            category.slug = slugify(cat_name) + str(category.id)
            category.save()
            messages.success(request, 'A new Category has been created!')
            return redirect('menu-builder')            
        else:
            print(form.errors)
    else:
        form = CategoryForm()    
    context = {
        'form': form
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def edit_category(request, slug=None):
    vendor = get_vendor(request)
    category = Category.objects.get(vendor=vendor,slug=slug)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category details have been Updated!')
            return redirect('menu-builder')
        else:
            print(form.errors)
    else:            
        form = CategoryForm(instance=category)
    
    context = {
        'category':category,
        'form':form
    }
    
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def delete_category(request, slug=None):
    vendor = get_vendor(request)
    category = Category.objects.get(vendor=vendor, slug=slug)
    category.delete()
    messages.success(request, 'Category has been deleted!')
    return redirect('menu-builder')
    

@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def add_food_item(request):
    form = FoodItemForm()  
    if request.method == 'POST':      
        vendor = get_vendor(request)  
        food_title = request.POST['food_title']        
        slug = slugify(food_title)
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        
        
        cat_pk = request.POST['category']
        category = Category.objects.get(pk=cat_pk)
               
       
        food_item = FoodItem.objects.create(vendor=vendor,category=category, food_title=food_title, slug=slug, description=description, price=price, image=image)
        food_item.save()
        messages.success(request, 'A new Food Item has been added!')
        return redirect('items-by-category', category.slug)       
        
    else:
        form = FoodItemForm()    
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form':form
    }
    return render(request, 'vendor/add_food_item.html', context)


@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def delete_food_item(request, slug=None):
    food_item = FoodItem.objects.get(slug=slug)
    category_slug = food_item.category.slug
    messages.success(request, 'Successfully deleted the Food Item')
    food_item.delete()
    return redirect('items-by-category',category_slug)


@login_required(login_url='login-user')
@user_passes_test(if_vendor_user)
def edit_food_item(request, slug=None):
    food_item = FoodItem.objects.get(slug=slug)
    if request.method == 'POST':
        vendor = get_vendor(request)  
        food_title = request.POST['food_title']        
        slug = slugify(food_title)
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES['image']
        
        food_item.vendor = vendor
        food_item.food_title = food_title
        food_item.slug = slug
        food_item.description = description
        food_item.price = price
        food_item.image = image
        
        food_item.save()
        messages.success(request, 'Food item details have been updated')
        return redirect('items-by-category', food_item.category.slug)
    else:            
        form = FoodItemForm(instance=food_item)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'food_item':food_item,
        'form':form
    }
    return render(request, 'vendor/edit_food_item.html',context)




# opening hours
def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    
    context = {
        'opening_hours': opening_hours,
        'form': form
    }
    return render(request, 'vendor/opening_hours.html', context)

def add_hours(request):    
    if request.user.is_authenticated:
        if  request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST['day']
            from_hour = request.POST['from_hour']
            to_hour = request.POST['to_hour']
            is_closed = request.POST['is_closed']
            print(is_closed)
            if is_closed == 'false':
                is_closed = False
            else:
                is_closed = True    
                
            print(day, from_hour, to_hour, is_closed)
            # add the data into the database
            try:
                instance = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                instance.save()
                
                if instance:
                    get_instance = OpeningHour.objects.get(id=instance.id)
                    print(get_instance)
                    if get_instance.is_closed:    # if true
                        data = {
                            'success': "Model instance created. It is closed",
                            'day': get_instance.get_day_display(),   
                            'is_closed': get_instance.is_closed,
                            'id': get_instance.pk                      
                        }
                        return JsonResponse(data)
                    else: # if false                        
                        data = {
                            'success': "Model Instance created. Not Closed",
                            'day': get_instance.get_day_display(),
                            'from_hour': get_instance.from_hour,
                            'to_hour': get_instance.to_hour,
                            'is_closed': get_instance.is_closed,
                            'id': get_instance.pk  
                        }
                        return JsonResponse(data)
        
            except IntegrityError as e :
                return JsonResponse({
                    'failure': f"Hours from {from_hour} - {to_hour} on this day exists!",
                    'error' :str(e)
                })           
        else:
            data = {
                'failure': "Not an Ajax Request"
            }
            return JsonResponse(data)
            
    else:
        data = {
            'failure': "Please Login to Contienue"
        }
        return JsonResponse(data)
    
    

def remove_add_hours(request, pk=None):
    if  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # query the hour instance and delete it
        hour = OpeningHour.objects.get(pk=pk)
        hour.delete()
        return JsonResponse({
            'success': 'Deleted Successfully!',
            'hour_id': pk
        })
    else:        
        return JsonResponse({
            'failure':'Not an Ajax Request',
            
        })
