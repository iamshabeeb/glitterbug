
from django.http import JsonResponse
from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct,Payment
import razorpay
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False,order_number=body['orderID'])
    #store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        payment_method = body['payment_method'],
        amount_paid = body['amount'],
        status = body['status'],
        payment_signature = body['razorpay_signature'],
        razorpay_order_id = body['razorpay_order_id']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


    # reduce the quantity of sold product

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear the cart 

    CartItem.objects.filter(user=request.user).delete()

    # send order recieved email to customer

    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_recieved_email.html',{
        'user':request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # send order number and transaction id back to send data method via json response

    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }

    return JsonResponse(data)

def place_order(request, total = 0, quantity = 0):
    current_user = request.user


    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <=0:
        return redirect ('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total+tax

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing informations inside the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # genarate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            client = razorpay.Client(auth=("rzp_test_UnazQZ1TKJ19pH", "eGswxgNBeY4CFVVzLlko4Z3d"))
            DATA = {
                "amount": data.order_total * 100,
                "currency": "INR",
                "payment_capture": 1,
                # "receipt": "receipt#1",
                # "notes": { 
                #     "key1": "value3",
                #     "key2": "value2"
                # }
            }
            payment = client.order.create(data=DATA)
            print(order_number)
            print(payment)
            

            order=Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'payment':payment,

            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect ('checkout')



def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render (request, 'orders/order_complete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect ('home')
    
        
    
        
        



    