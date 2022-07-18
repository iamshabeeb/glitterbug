from django.shortcuts import render
from accounts.models import Account
from orders.models import Order
from category.models import Category
from store.models import Product,Variation
from adminpanel.forms import AddProductForm

# Create your views here.

def adminpanel(request):
    user = request.user
    context = {
        'user':user
    }
    return render(request, 'adminpanel/adminpanel.html',context)

def user_table(request):
    user_details = Account.objects.all()
    context = {
        'user_details':user_details
    }
    return render (request, 'adminpanel/user_table.html',context)

def banned_user(request):
    return render (request, 'adminpanel/banned_user.html')

def view_orders(request):
    order_details = Order.objects.all()
    context = {
        'order_details':order_details,
    }
    return render (request, 'adminpanel/view_orders.html',context)

def view_category(request):
    category_details = Category.objects.all()
    context = {
        'category_details':category_details,
    }
    return render (request, 'adminpanel/view_category.html',context)

def view_products(request):
    product_details = Product.objects.all()
    context = {
        'product_details':product_details,
    }
    return render (request, 'adminpanel/view_products.html', context)

def view_variations(request):
    variation_details = Variation.objects.all()
    context = {
        'variation_details':variation_details,
    }
    return render (request, 'adminpanel/view_variations.html', context)

def add_product(request):
    form = AddProductForm()
    context ={
        'form':form,
    }
    return render(request, 'adminpanel/add_productform.html',context)



