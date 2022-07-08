from base64 import urlsafe_b64decode
from email.message import EmailMessage
from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from carts.views import _cart_id
from carts.models import Cart,CartItem
import requests


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'please activate your acccount'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Thank you for register with us , We have sent a verification email to you please verify it  ')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user=auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cartitem_exist = CartItem.objects.filter( cart = cart ).exists()
                if is_cartitem_exist:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    existing_var_list=[]
                    id = []
                    for item in cart_item:
                        existing_variations = item.variations.all()
                        existing_var_list.append(list(existing_variations))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in existing_var_list:
                            index = existing_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print(query)
                params = dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect( 'dashboard')
                
        else:
            messages.error(request, 'invalid login credentials...')
            return redirect ('login')
    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are successfully logged out.')
    return redirect('login')


def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation your account is activated')
        return redirect('login')

    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact = email)
            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'reset your password'
            message = render_to_string('accounts/reset_password_emial.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'password reset email has been sent to your email address')
            return redirect('login')




        else:
            messages.error(request, 'Account does not exists')
            return redirect ('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'this link has been expired')   
        return redirect ('login') 


def resetPassword(request):
    if request.method =='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successfull')
            return redirect('login')

        else:
            messages.error(request, 'password do not match')
            return redirect('resetPassword')
    else:
        return render (request, 'accounts/resetPassword.html')
      


