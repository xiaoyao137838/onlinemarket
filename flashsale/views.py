from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FlashSale, FlashOrder
from order.models import Payment
from vendor.models import OpeningHour, Product
from market.models import Tax
from .context_processors import flash_sale_order
from accounts.models import User, UserProfile
from vendor.models import Vendor, Product
from .forms import SaleForm, SaleOrderForm
from .utils import generate_order_no, get_role_url
from django.contrib import messages
from datetime import datetime, date
import json

# Create your views here.

def get_vendor(request):
    return Vendor.objects.get(user=request.user)

def flashsales(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug_name=vendor_slug)
    flashsales = FlashSale.objects.filter(vendor=vendor, is_active=True)
    context = {
        'flashsales': flashsales,
        'flashsale_count': flashsales.count()
    }
    return render(request, 'flashsales/flashsales.html', context)
    
def add_flashsale(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        sale_form = SaleForm(request.post)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.vendor = get_vendor(request)
            sale.save()
            messages.success(request, 'The new flash sale is added')
            return redirect('/products')
        else:
            messages.error(request, 'Some fields are not correct')
            context = {
                'sale_form': sale_form
            }
            return render(request, 'flashsales/new.html', context)

    init = {
        'old_price': product.price,
        'new_price': product.price,
        'from_time': datetime.now(),
        'to_time': datetime.now()
    }    
    sale_form = SaleForm(initial=init)
    context = {
        'sale_form':sale_form
    }
    return render(request, 'flashsales/new.html', context)
    
def delete_flashsale(request, id):
    flashsale = get_object_or_404(FlashSale, id=id)
    flashsale.delete()
    messages.info(request, 'The flash sale is deleted successfully')
    vendor = get_vendor(request)
    return redirect(f'/{ vendor.slug_name }/flash_sales')

def flashsale(request, id):
    url = get_role_url(request)
    return redirect(url + str(id))


def flashsale_vendor(request, id):
    flashsale = get_object_or_404(FlashSale, id=id)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST, instance=flashsale)
        if sale_form.is_valid():
            sale_form.save()
            messages.success(request, 'The flash sale is updated successfully')
            return redirect(f'/flash_sales/v/{id}')
        else:
            messages.error('Some fields are not correct')
            context = {
                'sale_form': sale_form,
                'flashsale': flashsale
            }
            return render(request, 'flashsales/flashsale.html', context)
        
    sale_form = SaleForm(instance=flashsale)
    context = {
        'sale_form': sale_form,
        'flashsale': flashsale
    }
    return render(request, 'flashsales/flashsale_vendor.html', context)

def flashsale_customer(request, id):
    flashsale = get_object_or_404(FlashSale, id=id)
    vendor = flashsale.vendor 
    product = flashsale.product 
    opening_hours = OpeningHour.objects.filter(vendor=vendor)
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hour = opening_hours.filter(day=today).order_by('from_time')
    
    context = {
        'flashsale': flashsale,
        'vendor': vendor,
        'product': product,
        'opening_hours': opening_hours,
        'current_opening_hour': current_opening_hour
    }

    return render(request, 'flashsales/flashsale_customer.html', context)

def select_flash_sale(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            flash_sale_id = request.GET['flash_sale_id']
            try:
                flash_sale = FlashSale.objects.get(id=flash_sale_id)
                product = flash_sale.product
                sub_amount = flash_sale.new_price
                tax_obj = Tax.objects.get(tax_type='Tax')
                tax_amount = sub_amount * float(tax_obj.percentage) / 100
                tax_data = {tax_obj.tax_type: { str(tax_obj.percentage): tax_amount }}
                total_amount = sub_amount + tax_amount
                try:
                    flash_order = FlashOrder.objects.get(customer=request.user, flash_sale=flash_sale)
                    return JsonResponse({
                        'status': 'error',
                        'message': 'The flash sale is selected before'
                    })
                except:
                    flash_order = FlashOrder.objects.create(
                        customer=request.user,
                        flash_sale=flash_sale,
                        product=product,
                        sub_amount=sub_amount,
                        tax_amount=tax_amount,
                        total_amount=total_amount,
                        tax_data=json.dumps(tax_data)
                    )
                    return JsonResponse({
                        'status': 'success',
                        'message': 'The flash sale is selected successfully'
                    })
            except:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No such flash sale exists'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Please login first'
        })
    
def checkout(request, id):
    profile = UserProfile.objects.get(user=request.user)
    init = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone,
        'email': request.user.email,
        'address': profile.address,
        'city': profile.city,
        'state': profile.state,
        'country': profile.country,
        'zip_code': profile.zip_code,
    }

    sale_order = flash_sale_order(request, id)['flash_sale_order']
    sale_order_form = SaleOrderForm(initial=init, instance=sale_order)
    context = {
        'sale_order_form': sale_order_form,
        'subtotal': sale_order.sub_amount,
        'tax': sale_order.tax_amount,
        'tax_dict': json.loads(sale_order.tax_data),
        'grand_total': sale_order.total_amount,
        'sale_order': sale_order
    }
    return render(request, 'flashsales/checkout.html', context)
    
def make_order(request, id):
    if request.method == 'POST':
        sale_order = flash_sale_order(request, id)['flash_sale_order']
        order_form = SaleOrderForm(request.POST, instance=sale_order)
        if order_form.is_valid():
            sale_order = order_form.save()        
            
            sale_order.order_no = generate_order_no(sale_order)
            sale_order.payment_method = request.POST['payment_method']
            sale_order.save()

            context = {
                'sale_order': sale_order,
                'subtotal': sale_order.sub_amount,
                'tax': sale_order.tax_amount,
                'tax_dict': json.loads(sale_order.tax_data),
                'grand_total': sale_order.total_amount
            }

            return render(request, 'flashsales/place_order.html', context)
        else: 
            messages.error('Some fields are not correct')
            context = {
                'order_form': order_form
            }
            return render(request, 'flashsales/checkout.html', context)
        
    return redirect('/flash_checkout')
    
def make_payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            payment_no = request.POST['transaction_id']
            sale_order_no = request.POST['sale_order_no']
            payment_method = request.POST['payment_method']

            try:
                sale_order = FlashOrder.objects.get(order_no=sale_order_no)
                flash_payment = Payment(
                    payment_no=payment_no,
                    customer=request.user,
                    amount=sale_order.total_amount,
                    method=payment_method,
                    status='Completed'
                )
     
                flash_payment.save()
                sale_order.payment = flash_payment
                sale_order.status = 1
                sale_order.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment is created successfully',
                    'sale_order_no': sale_order_no,
                    'transaction_id': payment_no
                })
            except:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Order does not exist'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Login first'
        })
    
def pay_done(request):
    sale_order_no = request.GET['sale_order_no']
    payment_no = request.GET['trans_id']
    sale_order = get_object_or_404(FlashOrder, order_no=sale_order_no)
    payment = get_object_or_404(Payment, payment_no=payment_no)

    context = {
        'sale_order': sale_order,
    }
    return render(request, 'flashsales/pay_done.html', context)

