from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages, auth
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import check_role_customer, check_role_vendor, get_role_url


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

@login_required(login_url='login')
def dashboard(request):
    role_url = get_role_url(request)
    return redirect(role_url)


@login_required(login_url='login') 
@user_passes_test(check_role_customer)
def customer_dashboard(request):   
    return render(request, 'customers/dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def vendor_dashboard(request):   
    return render(request, 'vendors/dashboard.html')