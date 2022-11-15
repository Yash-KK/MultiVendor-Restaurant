#MODELS
from .models import (
    Cart
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
    
    try:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            sub_total += item.fooditem.price * item.quantity
             
    except:
        cart_items = None 
    
     
    total = tax + sub_total
    
    return {
        'total': total,
        'sub_total':sub_total,
        'tax': tax
    }     