from unicodedata import category
from django.shortcuts import HttpResponse, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

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

#MODELS
from .models import (
    Vendor
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