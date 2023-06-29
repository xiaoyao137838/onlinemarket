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
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        logger.warning('Already login')
        messages.warning(request, 'Already login')
        return redirect('home')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.CUSTOMER
            user.save()

            mail_subject = 'Please activate your account'
            # send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_activation.html')
            messages.success(request, 'Successfully registered!')
            return redirect('login')
        else:
            logger.error(form.errors)
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
        logger.warning('Already login')
        messages.warning(request, 'Already login')
        return redirect('home')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            email = user_form.cleaned_data['email']
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.role = User.Role.VENDOR
            user.save()
            
            vendor = vendor_form.save(commit=False)
            vendor.user = user 
            vendor.profile = UserProfile.objects.get(user=user)
            vendor.slug_name = slugify(vendor.vendor_name) + '-' + str(user.id)
            vendor.save()

            mail_subject = 'Please activate your account'
            # send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_activation.html')
            messages.success(request, 'Vendor is registered successfully')
            return redirect('login')
        else:
            logger.error(vendor_form.errors)
            logger.error(user_form.errors)
            messages.error(request, 'Invalid vendor form')
            context = {
                'user_form': user_form,
                'vendor_form': vendor_form,
            }
            return render(request, 'accounts/registerVendor.html', context)
    
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
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.error(e)
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'This account is activated successfully')
        return redirect('dashboard')
    else:
        logger.error('Invalid activation link.')
        messages.error(request, 'Invalid activation link')
        return redirect('home')


def login(request):
    if request.user.is_authenticated:
        logger.warning('Already login')
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
            logger.error('Invalid credentials')
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
    logger.info('Logout successfully')
    messages.info(request, 'Logout successfully')
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        try: 
            user = User.objects.get(username=username)
            mail_subject = 'Reset password'
            # send_email_activation(request, user, mail_subject=mail_subject, email_template='emails/email_password_reset.html')
            logger.info('Email sent successfully for password reset')
            messages.success(request, 'Email sent successfully for password reset')
            return redirect('login')
        except Exception as e:
            logger.error(e)
            messages.error(request,'Account does not exist')
    
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_reset_request.html', context)

def password_reset_validator(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.error(e)
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        logger.info('Ready to reset password')
        messages.info(request, 'Please reset your password')
        return redirect('password_reset')
    else:
        logger.error('Invalid activation link')
        messages.error(request, 'Invalid activation link')
        return redirect('home')

def password_reset(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            id = request.session['uid']
            user = User.objects.get(id=id)
            user.set_password(password)
            user.is_active = True
            user.save()
            logger.info('Successfully reset password')
            messages.success(request, 'Successfully reset password')
            return redirect('login')
        else:
            logger.error('Passwords do not match')
            messages.error(request, 'Passwords do not match')

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
