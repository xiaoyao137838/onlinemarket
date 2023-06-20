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
from .redis_service import add_customer_to_limit, add_sale, create_flashsale, add_stock, is_customer_qualified, lock_stock
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
import json
import threading

try:
    from flashsale.kafka.kafka_service import producer
except:
    print('Producer does not exist')
    
# Create your views here.

def get_vendor(request):
    return Vendor.objects.get(user=request.user)

def flashsales(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug_name=vendor_slug)
    flashsales = FlashSale.objects.filter(vendor=vendor, is_active=True).order_by('created_at')
    context = {
        'flashsales': flashsales,
        'flashsale_count': flashsales.count()
    }
    return render(request, 'flashsales/flashsales.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)   
def add_flashsale(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.vendor = get_vendor(request)
            sale.product = product
            sale.save()

            create_flashsale(request, sale)
            messages.success(request, 'The new flash sale is added')
            return redirect('products')
        else:
            messages.error(request, 'Some fields are not correct')
            context = {
                'sale_form': sale_form,
                'product': product
            }
            return render(request, 'flashsales/new.html', context)

    init = {
        'old_price': product.price,
        'new_price': product.price,
        'from_time': datetime.now(),
        'to_time': datetime.now(),
    }    
    sale_form = SaleForm(initial=init)
    context = {
        'sale_form':sale_form,
        'product': product
    }
    return render(request, 'flashsales/new.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)    
def delete_flashsale(request, id):
    flashsale = get_object_or_404(FlashSale, id=id)
    flashsale.delete()
    messages.info(request, 'The flash sale is deleted successfully')
    vendor = get_vendor(request)
    return redirect('products')

@login_required(login_url='login')
def flashsale(request, id):
    url = get_role_url(request)
    return redirect(url + str(id))

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def flashsale_vendor(request, id):
    flashsale = get_object_or_404(FlashSale, id=id)
    if flashsale.vendor.user != request.user:
        return redirect(f'/flash_sales/c/{id}')
    
    if request.method == 'POST':
        sale_form = SaleForm(request.POST, instance=flashsale)

        if sale_form.is_valid():
            sale = sale_form.save()
            add_stock(request, sale)
            add_sale(request, sale)
            messages.success(request, 'The flash sale is updated successfully')
            return redirect(f'/flash_sales/v/{id}')
        else:
            messages.error(request, 'Some fields are not correct')
            context = {
                'sale_form': sale_form,
                'flashsale': flashsale
            }
            return render(request, 'flashsales/flashsale_vendor.html', context)
        
    sale_form = SaleForm(instance=flashsale)
    context = {
        'sale_form': sale_form,
        'flashsale': flashsale
    }
    return render(request, 'flashsales/flashsale_vendor.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def select_flash_sale(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            flash_sale_id = request.GET['flash_sale_id']
            print(is_customer_qualified(request, flash_sale_id))
            if is_customer_qualified(request, flash_sale_id):
                add_customer_to_limit(request.user.id, flash_sale_id)

                if lock_stock(flash_sale_id):
                    print('locked successfully')
                    data = dict(customer_id=request.user.id, flash_sale_id=flash_sale_id)
                    print(json.dumps(data))
                    producer.send(topic='create_order', 
                                  key=flash_sale_id.encode('utf-8'), 
                                  value=json.dumps(data).encode('utf-8'))
                    def delay_send():
                        producer.send(topic='check_pay_status', 
                                      key=flash_sale_id.encode('utf-8'), 
                                      value=json.dumps(data).encode('utf-8'))
                    timer = threading.Timer(2 * 60.0, delay_send)
                    timer.start()

                    return JsonResponse({
                        'status': 'success',
                        'message': 'The flashsale is selected successfully'
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Sorry, the flashsale is sold out'
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Sorry, you have selected before'
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

@login_required(login_url='login')    
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

@login_required(login_url='login') 
def make_order(request, id):
    if request.method == 'POST':
        sale_order = flash_sale_order(request, id)['flash_sale_order']
        if not sale_order:
            messages.warning(request, 'Please wait')
            return redirect('/flash_checkout')
        
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
            messages.error(request, 'Some fields are not correct')
            context = {
                'order_form': order_form
            }
            return render(request, 'flashsales/checkout.html', context)
        
    return redirect('/flash_checkout')

@login_required(login_url='login')    
def make_payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            payment_no = request.POST['transaction_id']
            sale_order_no = request.POST['sale_order_no']
            payment_method = request.POST['payment_method']

            try:
                sale_order = FlashOrder.objects.get(order_no=sale_order_no)
                if sale_order.status != 0:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'This order is not able to pay'
                    })
                
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

                data = { 'sale_order_no': sale_order_no }
                producer.send(topic='pay_done', 
                                key=sale_order_no.encode('utf-8'), 
                                value=json.dumps(data).encode('utf-8'))
                
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
    
@login_required(login_url='login')   
def pay_done(request):
    sale_order_no = request.GET['sale_order_no']
    payment_no = request.GET['trans_id']
    sale_order = get_object_or_404(FlashOrder, order_no=sale_order_no)
    payment = get_object_or_404(Payment, payment_no=payment_no)

    context = {
        'sale_order': sale_order,
    }
    return render(request, 'flashsales/pay_done.html', context)

