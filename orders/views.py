from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import simplejson as json
import datetime
from FoodOnlineMain.settings import KEY_ID, KEY_SECRET

#HELPERs
from marketplace.cp2 import (
    get_cart_amount
)
from accounts.utils import (
    order_confirmed_email
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
    Order,
    Payment,
    OrderedFood
)

#FORMS
from .forms import (
    OrderForm
)

#RAZORPAY
import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# Create your views here.
@login_required(login_url='login-user')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_count = cart_items.count()       
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
                       
            context = {
                'rzpay_id': rzpay_orderid,
                'order': order_instance,                
                'KEY_ID': KEY_ID,
                'cart_items': cart_items
            }            
            return render(request, 'orders/place_order.html', context)          
        else:
            print(form.errors)    
    return render(request, 'orders/place_order.html')

@login_required(login_url='login-user')
def payments(request):    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Fetch the data and store in Payments Database
        order_number = request.GET['order_number']
        transaction_id = request.GET['transaction_id']
        payment_method = request.GET['payment_method']
        status = request.GET['status']
        amount = request.GET['amount']
        
        # Payment model instance
        payment = Payment.objects.create(
            user=request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            status = status,
            amount = amount
        )
        payment.save()        
        # Fetching the order model and updating it
        order = Order.objects.get(order_number=order_number)
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        
        """Move the Cart Items to Ordered Food Model + Tabular Inline"""
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.user = request.user
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            
            ordered_food.save()          
                                
        """Send Email Confirmation to the Customer"""
        order_confirmed_email(user=request.user, email=order.email, order_number=order.order_number, trans_id=transaction_id)
        messages.success(request, 'Order Confirmation mail has been sent to you!')
        
        
        """Send Order Received Email to the Vendor and Clear the Cart"""
        # as of now, not doing the order received email but will clear the cart
        cart_items.delete()
        
        return JsonResponse({
            'order_number': order_number,
            'trans_id': transaction_id
        })     
       
    else:
        pass
    return HttpResponse("Payment Working")

@login_required(login_url='login-user')
def order_complete(request):
    print(request.path)
    trans_id = request.GET['trans_id']
    order_number = request.GET['order_num']
    
    
    # fetch order to fetch ordered food
    order = Order.objects.get(order_number=order_number, payment__transaction_id=trans_id)
    ordered_food = OrderedFood.objects.filter(order=order)
    
    sub_total = 0 
    for item in ordered_food:
        sub_total += item.amount
    
    tax_data = json.loads(order.tax_data)
    context = {
        'order': order,
        'trans_id': trans_id,
        'ordered_food': ordered_food,
        'tax_data': tax_data,
        
        'sub_total': sub_total
    }
    
    return render(request, 'orders/order_complete.html', context)

