from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from .context_processors import get_cart_counter, get_cart_amounts
from accounts.views import check_role_customer
from vendor.models import Vendor, Product, OpeningHour
from .models import CartItem
from order.models import Order
from datetime import date

# Create your views here.
def get_customer(request):
    return request.user

def marketplace(request):
    vendors = Vendor.objects.filter(is_verified=True, user__is_active=True)
    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'market/marketplace.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug_name=vendor_slug)
    products = Product.objects.filter(vendor=vendor)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_time')

    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today).order_by('from_time')

    user = request.user
    if user.is_authenticated:
        customer = get_customer(request)
        cart_items = CartItem.objects.filter(customer=customer)
    else: 
        cart_items = None

    context = {
        'vendor': vendor,
        'products': products,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        'cart_items': cart_items,
    }
    return render(request, 'market/vendor_detail.html', context)

#cart
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cart(request):
    user = request.user
    if user.role == 'Vendor':
        raise PermissionDenied
    
    customer = get_customer(request)
    cart_items = CartItem.objects.filter(customer=customer).order_by('created_at')

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'market/cart.html', context)


def add_cart(request, product_id):
    customer = get_customer(request)
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id=product_id)
                try:
                    cart_item = CartItem.objects.get(customer=customer, product=product)
                    cart_item.quantity += 1
                    cart_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Product is added to cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
                except:
                    cart_item = CartItem.objects.create(customer=customer, product=product, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'New cart item created', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'This product does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in'})
    

def deduce_cart(request, product_id):
    customer = get_customer(request)
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id=product_id)
                try:
                    cart_item = CartItem.objects.get(customer=customer, product=product)
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        return JsonResponse({'status': 'success', 'message': 'Product is deduced from cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
                    else:
                        cart_item.delete()
                        cart_item.quantity = 0
                        return JsonResponse({'status': 'success', 'message': 'Product is deduced from cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
                    
                except:
                    return JsonResponse({'status': 'failed', 'message': 'This product is not in cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': 0})
            except:
                return JsonResponse({'status': 'failed', 'message': 'This product does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in'})
                

def remove_cart(request, cart_id):
    if request.user.is_authenticated:
        customer = get_customer(request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                try:
                    cart_item = CartItem.objects.get(customer=customer, id=cart_id)
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Delete the item from cart',
                        'cart_counter': get_cart_counter(request),
                        'amounts': get_cart_amounts(request),
                    })
                except:
                    return JsonResponse({
                        'status': 'failed',
                        'message': 'Cart item does not exist in the cart',
                    })
            
        else:
            return JsonResponse({
                'status': 'failed',
                'message': 'Invalid request',
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Please log in first'
        })

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def checkout(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    context = {
        'cart_items': Cart_items,
    }
    return render(request, 'market/checkout.html', context)