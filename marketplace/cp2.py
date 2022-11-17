#MODELS
from .models import (
    Cart,
    Tax
)

def get_cart_count(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user = request.user)
            for cart in carts:
                cart_count += cart.quantity
        else:
            cart_count = 0
    except:
        cart_count = 0
    return {
        'cart_count': cart_count
    }
    
def get_cart_amount(request):
    total,sub_total,tax = 0,0,0
    tax_dict = {}
    try:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            sub_total += item.fooditem.price * item.quantity
        
        tax_type = Tax.objects.filter(is_active=True)
        for i in tax_type:
            tax_dict[str(i.tax_type)] = {
                str(i.tax_percentage) : round((i.tax_percentage*sub_total)/100,2)
                
            }
    
    except:
        cart_items = None 
    
    tax_sum = 0    
    for key, value in tax_dict.items():
        for i,j in value.items():
            tax_sum += j
             
    total = sub_total + tax_sum            
   
    return {
        'total': total,
        'sub_total':sub_total,
        'tax': tax_sum,
        'tax_dict': tax_dict
    }     