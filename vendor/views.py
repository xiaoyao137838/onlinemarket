from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from accounts.models import UserProfile
from order.models import Order, OrderedItem
from .models import Vendor, Product, OpeningHour
from accounts.forms import UserProfileForm
from .forms import VendorForm, ProductForm, OpeningHourForm 
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

# Create your views here.
def get_vendor(request):
    return Vendor.objects.get(user=request.user)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Vendor profile updated successfully')
            return redirect('vendor_profile')

    profile_form = UserProfileForm(instance=user_profile)
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': user_profile,
        'vendor': vendor,
    }
    return render(request, 'vendors/vendor_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_orders(request):
    vendor = get_vendor(request)
    orders = Order.objects.filter(vendors__in=[vendor.id]).order_by('created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'vendors/vendor_orders.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_order(request, order_id):
    order = Order.objects.get(id=order_id)
    vendor = get_vendor(request)

    if not order: 
        messages.error(request, 'No such order found')
        return redirect('vendor_orders')
    
    ordered_items = OrderedItem.objects.filter(order=order, product__vendor=vendor)
    context = {
        'order': order,
        'ordered_items': ordered_items,
        'subtotal': order.get_total_by_vendor()['subtotal'],
        'tax_data': order.get_total_by_vendor()['tax_dict'],
        'grand_total': order.get_total_by_vendor()['grand_total'],
    }
    return render(request, 'vendors/vendor_order.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def products(request):
    vendor = get_vendor(request)
    products = Product.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'products': products,
    }
    return render(request, 'vendors/products.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_product(request):
    vendor = get_vendor(request)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            name = product_form.cleaned_data['name']
            product = product_form.save(commit=False)
            product.vendor = vendor
            product.slug_name = slugify(name)
            product.save()
            messages.success(request, 'Add product successfully')
            return redirect('products')
    
    product_form = ProductForm()
    context = {
        'product_form': product_form,
    }
    return render(request, 'vendors/add_product.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product(request, id):
    vendor = get_vendor(request)
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            name = product_form.cleaned_data['name']
            product = product_form.save(commit=False)
            product.slug_name = slugify(name)
            product_form.save()
            messages.success(request, 'Product is updated successfully')
            return redirect('products')
    
    product_form = ProductForm(instance=product)
    context = {
        'product_form': product_form,
        'product': product,
    }
    return render(request, 'vendors/product.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_product(request, id):
    vendor = get_vendor(request)
    product = Product.objects.filter(id=id, vendor=vendor)

    if product:
        product.delete()
        messages.info(request, 'Product is deleted')
        return redirect('products')
    else:
        messages.error(request, 'No such product found')
        return redirect('products')
    
# Opening hours
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours(request):
    vendor = get_vendor(request)
    opening_hours = OpeningHour.objects.filter(vendor=vendor)
    opening_hour_form = OpeningHourForm()

    context = {
        'opening_hours': opening_hours,
        'opening_hour_form': opening_hour_form,
    }
    return render(request, 'vendors/opening_hours.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_opening_hour(request):
    vendor = get_vendor(request)
    print('add opening hour is running')
    if request.method == 'POST' and request.header.get('x-requested_with') == 'XMLHttpRequest':
        day, from_hour, to_hour, is_closed = request.POST
        try:
            opening_hour = OpeningHour.objects.create(vendor=vendor, day=day, from_time=from_hour, to_time=to_hour, is_closed=is_closed)

            if opening_hour:
                if opening_hour.is_closed:
                    response = {
                        'status': 'success',
                        'id': opening_hour.id,
                        'day': opening_hour.get_day_display(),
                        'is_closed': 'Closed',
                    }

                else:
                    response = {
                        'status': 'success',
                        'id': opening_hour.id,
                        'day': opening_hour.get_day_display(),
                        'from_hour': opening_hour.from_time,
                        'to_hour': opening_hour.to_time,
                    }
            return JsonResponse(response)
        
        except IntegrityError as e:
            response = {
                'status': 'failed',
                'message': from_time + '-' + to_time + 'already exists for this day'
            }
            return JsonResponse(response)

    else:
        HttpResponse('Invalid request')
 
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_opening_hour(request, id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        opening_hour = get_object_or_404(OpeningHour, id=id)
        opening_hour.delete()
        return JsonResponse({'status': 'success', 'id': id})