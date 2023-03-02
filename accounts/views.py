from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib import messages, auth

from order.models import Order
from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import check_role_customer, check_role_vendor, get_role_url, send_email_activation
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import simplejson as json
from datetime import datetime


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already login')
        return redirect('home')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.role = User.CUSTOMER
            user.save()

            mail_subject = 'Please activate your account'
            send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_activation.html')
            messages.success(request, 'Successfully registered!')
            return redirect('registerUser')
        else:
            print(form.errors)
            context = {
                'form': form,
            }
        return render(request, 'accounts/registerUser.html', context)
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already login')
        return redirect('home')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save(commit=False)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user 
            vendor.profile = UserProfile.objects.get(user=user)
            vendor.slug_name = slugify(vendor.vendor_name) + '-' + str(user.id)
            vendor.save()

            mail_subject = 'Please activate your account'
            send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_activation.html')
            messages.success(request, 'Vendor is registered successfully')
            return redirect('login')
        else:
            messages.error(request, 'Invalid vendor form')
            return redirect('registerVendor') 
    
    user_form = UserForm()
    vendor_form = VendorForm()
    context = {
        'user_form': user_form,
        'vendor_form': vendor_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'This account is activated successfully')
        return redirect('dashboard')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('home')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already login')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
       
        if user:
            auth.login(request, user)
            messages.success(request, 'Login successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successfully')
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username=username)
        if user: 
            mail_subject = 'Reset password'
            send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_password_reset.html')
            messages.success(request, 'Email sent successfully for password reset')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('password_reset')
    
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_reset_request.html', context)

def password_reset_validator(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        return redirect('password_reset')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('home')

def password_reset(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password is reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('password_reset')
        
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_reset.html', context)
        


@login_required(login_url='login')
def dashboard(request):
    role_url = get_role_url(request)
    return redirect(role_url)


@login_required(login_url='login') 
@user_passes_test(check_role_customer)
def customer_dashboard(request):  
    orders = Order.objects.filter(customer=request.user, status='Completed').order_by('-created_at')
    recent_orders = orders[:5]
    context = {
        'orders_count': orders.count(),
        'orders': orders,
        'recent_orders': recent_orders,
    } 
    return render(request, 'customers/dashboard.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def vendor_dashboard(request):   
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(status='Completed', vendors__in=[vendor]).order_by('-created_at')
    recent_orders = orders[:5]

    revenue = 0
    for order in orders:
        revenue += order.get_total_by_vendor()['total']

    revenue_month = 0
    month = datetime.now().month
    orders_month = orders.filter(created_at__month=month)
    for order in orders_month:
        revenue_month += order.get_total_by_vendor()['total']

    context = {
        'orders_count': orders.count(),
        'orders': orders,
        'recent_orders': recent_orders,
        'revenue': round(revenue, 2),
        'revenue_month': round(revenue_month, 2),
    }
    return render(request, 'vendors/dashboard.html', context)
