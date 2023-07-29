from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from accounts.utils import send_notification
from vendor.models import Vendor
from django.http import JsonResponse, HttpResponse
from market.context_processors import get_cart_amounts
from order.models import Order, Payment, OrderedItem
from .forms import OrderForm
from market.models import CartItem, Tax
from datetime import datetime
import simplejson as json
import logging

logger = logging.getLogger(__name__)
# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    get_tax = Tax.objects.all()
    vendor_list = []
    sub_dict = {}
    total_dict = {}

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
 
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = request.user
            order.payment_method = request.POST['payment_method']

            for item in cart_items:
                if item.product.vendor not in vendor_list:
                    vendor_list.append(item.product.vendor.pk)

            cart_amounts = get_cart_amounts(request)
            order.sub_amount = cart_amounts['subtotal']
            order.tax_amount = cart_amounts['tax']
            order.total_amount = cart_amounts['grand_total']
            order.tax_data = json.dumps(cart_amounts['tax_dict'])
            order.save()

            order.order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(order.pk)
            order.vendors.add(*vendor_list)
            for item in cart_items:
                if (item.product.vendor.pk) not in sub_dict:
                    sub_dict[(item.product.vendor.pk)] = item.quantity * item.product.price
                else:
                    sub_dict[(item.product.vendor.pk)] += item.quantity * item.product.price 

            for key in sub_dict:
                sub_tax = {}
                for i in get_tax:
                    sub_tax[i.tax_type] = {str(i.percentage): round(float(i.percentage) * sub_dict[key] / 100, 2)}
                total_dict[key] = {str(sub_dict[key]) : sub_tax}
            order.total_data = json.dumps(total_dict)
            order.save()
           
            context = {
                'cart_items': cart_items,
                'order': order,
            }
            return render(request, 'order/place_order.html', context)
        
    return redirect('checkout')

@login_required(login_url='login')
def make_payment(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_no = request.POST['order_no']
        transaction_id = request.POST['transaction_id']
        payment_method = request.POST['payment_method']
        status = request.POST['status']

        try:
            order = Order.objects.get(customer=request.user,order_no=order_no)
            amount = order.total_amount

            payment = Payment.objects.create(
                payment_no = transaction_id,
                method = payment_method,
                customer = request.user,
                amount = amount,
                status = status
            )
            payment.save()
            
            order.payment = payment
            order.payment_method = payment_method
            order.status = 'Completed'
            order.save()

            #move items to ordered items
            cart_items = CartItem.objects.filter(customer=request.user)
            for item in cart_items:
                ordered_item = OrderedItem(
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity,
                    amount = item.quantity * item.product.price,
                    customer = request.user,
                    order = order,
                    payment = payment
                )
                ordered_item.save()

            # Clean the cart
            cart_items.delete()
            logger.info('Cart items are moved to ordered items and deleted.')

            # send email to customer
            ordered_products = OrderedItem.objects.filter(order=order)
            subtotal = order.sub_amount
            tax_data = json.loads(order.tax_data) if order.tax_data else {}
            total = order.total_amount

            mail_subject = 'Thank you for your order'
            mail_template = 'order/customer_order_email.html'
            context = {
                'customer': request.user,
                'order': order,
                'to_email': order.email,
                'ordered_products': ordered_products,
                'subtotal': subtotal,
                'tax_data': tax_data,
                'total': total,
                'domain': get_current_site(request),
            }
            # send_notification(mail_subject, mail_template, context)

            # send emails to vendors
            mail_subject = 'You receive a new order'
            mail_template = 'order/vendor_order_email.html'
            total_data = json.loads(order.total_data) if order.total_data else {}
            tax = Tax.objects.get(tax_type='Tax')
            for key in total_data:
                vendor = Vendor.objects.get(id=key)
                ordered_products = OrderedItem.objects.filter(product__vendor=vendor, order=order)
                subtotal = 0
                for item in ordered_products:
                    subtotal += item.quantity * item.price
                
                tax_amount = round(float(tax.percentage) * subtotal / 100, 2)
                context = {
                    'vendor': vendor,
                    'order': order,
                    'to_email': vendor.user.email,
                    'ordered_products': ordered_products,
                    'subtotal': subtotal,
                    'tax_data': {key: {tax.tax_type: {str(tax.percentage): tax_amount}}},
                    'total': subtotal + tax_amount,
                    'domain': get_current_site(request),
                }
                
                # send_notification(mail_subject, mail_template, context)

            logger.info('The payment is successful.')
            return JsonResponse({
                'status': 'success',
                'order_no': order.order_no,
                'transaction_id': transaction_id,
            })
        except Exception as e: 
            logger.error(e)
            logger.error('This order does not exist.')
            return JsonResponse({
            'status': 'failed',
            'message': 'This order does not exist.',
        })
    else:
        logger.warning('Invalid request.')
        return JsonResponse({
            'status': 'failed',
            'message': 'Invalid request',
        })

@login_required(login_url='login')
def payment_complete(request):
    order_no = request.GET['order_no']
    transaction_id = request.GET['trans_id']

    try:
        order = Order.objects.get(order_no=order_no, payment__payment_no=transaction_id, status='Completed')
        ordered_items = OrderedItem.objects.filter(order=order)

        context = {
            'order': order,
            'ordered_items': ordered_items,
            'subtotal': order.sub_amount,
            'tax_data': order.tax_data,
            'tax_amount': order.tax_amount,
            'total': order.total_amount,
            'user_name': request.user.username,

            'first_name': order.first_name,
            'last_name': order.last_name,
            'phone': order.phone,
            'email': order.email,
            'address': order.address,
            'city': order.city,
            'state': order.state,
            'country': order.country,
            'zip_code': order.zip_code,
        }
        return render(request, 'order/payment_complete.html', context)

    except Exception as e:
        logger.error(e)
        return redirect('home')

