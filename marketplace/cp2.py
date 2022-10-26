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