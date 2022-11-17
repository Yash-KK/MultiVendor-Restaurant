from django.shortcuts import render, redirect
from django.http import HttpResponse
import simplejson as json
import datetime
from FoodOnlineMain.settings import KEY_ID, KEY_SECRET
#HELPERs
from marketplace.cp2 import (
    get_cart_amount
)
def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    order_number = current_datetime + str(pk)
    return order_number

# MODELS
from marketplace.models import (
    Cart
)
from .models import (
    Order
)

#FORMS
from .forms import (
    OrderForm
)

#RAZORPAY
import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# Create your views here.
def place_order(request):
    cart_items_count = Cart.objects.filter(user=request.user).count()       
    if cart_items_count <=0:
        return redirect('market-place')
    
    cart_amount = get_cart_amount(request)
    total = cart_amount['total']
    # sub_total = cart_amount['sub_total']
    tax_dict = cart_amount['tax_dict']
    tax = cart_amount['tax']
    
    
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():            
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']           
            
            order.user = request.user
            order.total = total
            order.total_tax = tax
            order.tax_data = json.dumps(tax_dict)
            order.payment_method = request.POST['payment_method']
            order.order_number = '123'
            order.save()
            
            order.order_number = generate_order_number(order.id)
            order.save()
            
            # Razorpay related
            DATA = {
                "amount": int((order.total)*100),
                "currency": "INR",
                "receipt": "receipt"+str(order.id),               
            }
            razorpay_order = client.order.create(data=DATA)
            rzpay_orderid = razorpay_order['id']
            
            order_instance = Order.objects.get(id=order.id)
            print(order_instance)
            
            
            context = {
                'rzpay_id': rzpay_orderid,
                'order': order_instance,
                
                'KEY_ID': KEY_ID,
                # 'KEY_SECRET': KEY_SECRET
            }
            
            return render(request, 'orders/place_order.html', context)
                        
            
                   
        else:
            print(form.errors)    
    return render(request, 'orders/place_order.html')


