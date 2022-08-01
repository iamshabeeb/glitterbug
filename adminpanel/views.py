from django.shortcuts import redirect, render
from accounts.models import Account
from orders.models import Order, OrderProduct,Payment
from category.models import Category
from store.models import Product,Variation
from adminpanel.forms import AddProductForm,EditCategory
from django.db.models import Q
from django.db.models import Sum,Count
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models.functions import TruncMonth,TruncMinute,TruncDay
import datetime
# Create your views here.

def adminpanel(request):
    chart_year = datetime.date.today().year
    chart_month = datetime.date.today().month
    user = request.user
    earnings = Order.objects.filter(is_ordered=True).aggregate(sum=Sum('order_total'))['sum']
    rounded_amount = round(int(earnings))
    profit = round (int(rounded_amount * 60/100))
    sold_products = OrderProduct.objects.all().count()
    target = 45
    percentage = target *  (sold_products)/100
    tops_cat        = Category.objects.get(category_name='tops')
    tops_name       = tops_cat.category_name
    tops_count      = tops_cat.count_sold
    
    # sets_cat        = Category.objects.get(category_name='sets')
    # sets_name       = sets_cat.category_name
    # sets_count      = sets_cat.count_sold

    # outwear_cat     = Category.objects.get(category_name='outwear')
    # outwear_name    = outwear_cat.category_name
    # outwear_count   = outwear_cat.count_sold
    
    onepiece_cat = Category.objects.get(category_name='onepiece')
    onepiece_name    = onepiece_cat.category_name
    onepiece_count   = onepiece_cat.count_sold

    dresses_cat = Category.objects.get(category_name='Dresses')
    dresses_name    = dresses_cat.category_name
    dresses_count   = dresses_cat.count_sold
    
    #getting daily revenue
    daily_revenue = Order.objects.filter(                     
        created_at__year=chart_year,created_at__month=chart_month
    ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

    day=[]
    revenue=[]
    for i in daily_revenue:
        day.append(i['day'].minute)
        revenue.append(int(i['sum']))

    context = {
        'user':user,
        'rounded_amount':rounded_amount,
        'profit':profit,
        'sold_products':sold_products,
        'target':target,
        'percentage':percentage,
        # 'sets_count':sets_count,
        # 'sets_name':sets_name,
        'tops_name':tops_name,
        'tops_count':tops_count,
        # 'outwear_name':outwear_name,
        # 'outwear_count':outwear_count,
        'onepiece_name':onepiece_name,
        'onepiece_count':onepiece_count,
        'dresses_name':dresses_name,
        'dresses_count':dresses_count,
        'day':day,
        'revenue':revenue,

    }
    return render(request, 'adminpanel/adminpanel.html',context)

def user_table(request):
    user_details = Account.objects.filter(is_active=True)
    paginator = Paginator(user_details, 1)
    page = request.GET.get('page')
    paged_user = paginator.get_page(page)
    context = {
        'user_details':paged_user,
    }
    return render (request, 'adminpanel/users/user_table.html',context)


def ban_user(request, id):
    if request.method == 'POST':
        user = Account.objects.get(id = id)
        if request.user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
    return redirect('user_table')

def banned_user(reqest):
    user_banned = Account.objects.filter(is_active = False)
    context = {
        'user_banned':user_banned,
    }
    return render (reqest, 'adminpanel/users/banned_user.html', context)

def unban_user(request, id):
    if request.method=='POST':
        user = Account.objects.get(id = id)
        user.is_active = True
        user.save()
    return redirect ('banned_user')



def view_orders(request):
    order_details = Order.objects.filter(status = 'New')
    context = {
        'order_details':order_details,
    }
    return render (request, 'adminpanel/orders/view_orders.html',context)

def view_category(request):
    category_details = Category.objects.filter(is_available = True)
    context = {
        'category_details':category_details,
    }
    return render (request, 'adminpanel/category/view_category.html',context)

def unlisted_category(request):
    category_details = Category.objects.filter(is_available = False)
    context = {
        'category_details':category_details,
    }
    return render (request, 'adminpanel/category/unlisted_category.html',context)

def unlist_category(request, id):
    category = Category.objects.get(id = id)
    category.is_available = False
    category.save()
    return redirect('view_category')

def list_category(request, id):
    category = Category.objects.get(id=id)
    category.is_available = True
    category.save()
    return redirect('unlisted_category')

def edit_category(request, id):
    category = Category.objects.get(id=id)
    if request.method=='POST':
        form = EditCategory(request.POST,request.FILES,instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_category')
    else:
        form = EditCategory(instance=category)
    context ={
        'form':form,
    }
    return render(request, 'adminpanel/category/edit_category.html',context)

def add_category(request):
    if request.method=='POST':
        form = EditCategory(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        form = EditCategory()
        context ={
            'form':form,
        }
        return render(request, 'adminpanel/category/add_category.html',context)
    else:
        form = EditCategory()
        context ={
            'form':form,
        }
        
    return render(request, 'adminpanel/category/add_category.html', context)

def view_products(request):
    product_details = Product.objects.filter(is_available = True)
    context = {
        'product_details':product_details,
    }
    return render (request, 'adminpanel/products/view_products.html', context)

def unlisted_products(request):
    product_details = Product.objects.filter(is_available = False)
    context = {
        'product_details':product_details,
    }
    return render (request, 'adminpanel/products/unlisted_products.html', context)

def view_variations(request):
    variation_details = Variation.objects.all()
    context = {
        'variation_details':variation_details,
    }
    return render (request, 'adminpanel/variations/view_variations.html', context)



def add_product(request): 
    if request.method=='POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        form = AddProductForm()
        context ={
            'form':form,
        }
        return render(request, 'adminpanel/products/add_productform.html',context)
    else:
        form = AddProductForm()
        context ={
            'form':form,
        }
        return render(request, 'adminpanel/products/add_productform.html',context)


def edit_product(request,id):
    product = Product.objects.get(id=id)
    if request.method=='POST':
        form = AddProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')
    else:
        form = AddProductForm(instance=product)
    context ={
        'form':form,
    }
    return render(request, 'adminpanel/products/edit_product.html',context)

def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.is_available=False
    product.save()
    return redirect ('view_products')  


def list_products(request, id):
    product = Product.objects.get(id = id)
    product.is_available = True
    product.save()
    return redirect('unlisted_products')









def search_user(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = Account.objects.filter(first_name__icontains = keyword)
    context = {
        'users':users
    }
    return render(request, 'adminpanel/search/search_user.html', context)

def paginator (request):
    user = Account.objects.all().filter(is_active=True)

def accept_orders(request,id):
    if request.method == 'POST':
        orders = Order.objects.get(id=id)
        orders.status = 'Accepted'
        orders.save()
        return redirect ('view_orders')

def accepted_orders_list (request):

    accepted_orders = Order.objects.filter(status='Accepted')
    context = {
        'accepted_orders':accepted_orders,
    }
    return render (request, 'adminpanel/orders/accepted_orders.html',context)

def completed_order(request, id):
    if request.method == 'POST':
        orders = Order.objects.get(id=id)
        orders.status='Completed'
        orders.save()
    return redirect('accepted_orders')

def completed_orders_list(request):
    completed = Order.objects.filter(status='Completed')
    context = {
        'completed':completed,
    }
    return render(request, 'adminpanel/orders/completed_orders_list.html',context)

def cancel_order(request, id):
    if request.method== 'POST':
        order = Order.objects.get(id=id)
        order.status='New'
        order.save()
    return redirect ('completed_orders_list')


    







 












