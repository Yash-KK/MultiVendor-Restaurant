from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
#helper
from .cp2 import (
    get_cart_amount,
    get_cart_count
)

#MODELS
from vendor.models import (
    Vendor
)
from menu.models import (
    Category,
    FoodItem
)
from marketplace.models import (
    Cart
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
    
    if request.user.is_authenticated:        
        cart = Cart.objects.filter(user=request.user)
    else:
        cart = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):  
   if request.user.is_authenticated:
       # check if the request is ajax
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # try to get the food item
            try:
                print(f"{food_id}: {type(food_id)}")
                fooditem = FoodItem.objects.get(id=food_id)
                print(fooditem)
                # try to get the cart: if exist, increase the quantity or create food item
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    print("check cart to increase quantity")
                    # increase the cart quantity
                    check_cart.quantity +=1
                    check_cart.save()         
                    return JsonResponse({'status': 'success!',
                                         'message': "Increased the quantity!",
                                         'cart_counter': get_cart_count(request),
                                         'item_quantity': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})      
                except:
                    # create new cart
                    print("create cart")

                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    check_cart.save()
                    
                    print("Did is save? Yes")
                    return JsonResponse({'status': 'success!',
                                         'message': "added food to cart",
                                         'cart_counter': get_cart_count(request), 
                                         'item_quantity': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})      
                
            except:    
                print("Food item does not exist!")            
                data = {
                    'status': 'Failure!',
                    'message': "Food item does not exist!"
                }
                return JsonResponse(data)
       else:
           data = {
           'status': 'Failed!',
           'message': "request is not ajax"
       }
       return JsonResponse(data)
           
   else:
       data = {
           'status': 'login_required',
           'message': "Please login to continue"
       }
       return JsonResponse(data)
    

def decrease_cart(request, food_id):
    current_user = request.user
    if current_user.is_authenticated:
        fooditem = FoodItem.objects.get(id=food_id)
        try:
            try:
                check_cart = Cart.objects.get(user=current_user, fooditem=fooditem)
                if check_cart.quantity >1:
                    check_cart.quantity -=1
                    check_cart.save()
                    return JsonResponse({"status":'success!', 
                                         'message':'Decreased the quantity',
                                         'cart_counter': get_cart_count(request), 
                                         'item_quantity':check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})
                else:
                    check_cart.delete() 
                    quantity = 0
                    return JsonResponse({"status":'success!', 
                                         'message':'Deleted the cart item',
                                         'cart_counter': get_cart_count(request),
                                         'item_quantity':quantity,
                                         'cart_amount': get_cart_amount(request)})
   
            except:
                pass
        except:
            return JsonResponse({"status":'Failed!', 'message':'Food item does not exist!'})

    else:
        return JsonResponse({"status":'login_required', 'message':'Please login to continue'})

@login_required(login_url='login-user')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart_item(request, cart_item_id=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
        cart_item = Cart.objects.get(id=cart_item_id)
        cart_item.delete()
           
        return JsonResponse({"success":"deleted the cart item", 
                             'cart_item_id': cart_item_id, 
                             'cart_counter': get_cart_count(request),
                             'cart_amount':get_cart_amount(request)}
                            )
    else:
        return JsonResponse({"failure":"Invalid Request!"})