import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import UserProfile
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from order.forms import OrderForm
from .context_processors import get_cart_counter, get_cart_amounts
from accounts.views import check_role_customer
from vendor.models import Vendor, Product, OpeningHour
from .models import CartItem, Review
from order.models import Order
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def get_customer(request):
    return request.user

def marketplace(request):
    logger.info('This is to show the vendor list.')
    vendors = Vendor.objects.filter(is_verified=True, user__is_active=True)
    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'market/marketplace.html', context)

def search(request):
    if 'address' not in request.GET:
        return redirect('marketplace')
    
    keyword = request.GET['keyword']
    address = request.GET['address']
    radius = request.GET['radius']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
  
    vendor_ids_products = Product.objects.filter(name__icontains=keyword, is_available=True).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(Q(id__in=vendor_ids_products, user__is_active=True, is_verified=True) | Q(vendor_name__icontains=keyword, user__is_active=True, is_verified=True))

    if latitude and longitude and radius:
        pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        vendors = vendors.filter(profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance("profile__location", pnt)).order_by("distance")

        for vendor in vendors:
            vendor.kms = round(vendor.distance.km, 1) # type: ignore

    context = {
        'vendors': vendors,
        'vendor_count': vendors.count(),
        'target_location': address,
    }
    return render(request, 'market/marketplace.html', context)

def all_opening_hours(vendor):
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_time')

    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today).order_by('from_time')

    return opening_hours, current_opening_hours

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, slug_name=vendor_slug)
    products = Product.objects.filter(vendor=vendor)
    opening_hours, current_opening_hours = all_opening_hours(vendor)

    user = request.user
    if user.is_authenticated:
        customer = get_customer(request)
        cart_items = CartItem.objects.filter(customer=customer)
    else: 
        cart_items = None
    
    profile_dict = {
        'address': vendor.profile.address,
        'longitude': vendor.profile.longitude,
        'latitude': vendor.profile.latitude
    }
    profile_json = json.dumps(profile_dict)
    context = {
        'vendor': vendor,
        'profile_json': profile_json,
        'products': products,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        'cart_items': cart_items,
    }
    return render(request, 'market/vendor_detail.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug_name=product_slug)
    opening_hours, current_opening_hours = all_opening_hours(product.vendor)

    if request.user.is_authenticated:
        customer = get_customer(request)
        cart_item = CartItem.objects.filter(customer=customer, product=product).first()
    else:
        Cart_item = None 

    context = {
        'product': product,
        'vendor': product.vendor,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        'item': cart_item,
    }
    return render(request, 'market/product_detail.html', context)

@login_required(login_url='login')
def cart(request):
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
                    cart_item.quantity += 1 # type: ignore
                    cart_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Product is added to cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
                except Exception as e:
                    logger.error(e)
                    cart_item = CartItem.objects.create(customer=customer, product=product, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'New cart item created', 'cart_counter': get_cart_counter(request), 'cart_product_qty': cart_item.quantity, 'amounts': get_cart_amounts(request)})
            except Exception as e:
                logger.error(e)
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
                    
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'status': 'failed', 'message': 'This product is not in cart', 'cart_counter': get_cart_counter(request), 'cart_product_qty': 0})
            except Exception as e:
                logger.error(e)
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
                except Exception as e:
                    logger.error(e)
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
def checkout(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    profile = UserProfile.objects.get(user=request.user)
    initial_values = {
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
    order_form = OrderForm(initial=initial_values)
    context = {
        'cart_items': cart_items,
        'order_form': order_form,
    }
    return render(request, 'market/checkout.html', context)


def add_review(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            try:
                posted_review = Review()
                posted_review.author = user
                product_id = request.POST['product_id']
                
                product = get_object_or_404(Product, id=product_id)
                posted_review.product = product
                posted_review.rating = request.POST['rating']
                posted_review.comment = request.POST['comment']
                try:
                    posted_review.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'New review is added successfully.',
                        'id': posted_review.id,
                        'rating': posted_review.rating,
                        'comment': posted_review.comment,
                        'username': posted_review.author.username
                    })
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({
                        'status': 'fail',
                        'message': 'Cannot add the review.'
                    })
            except Exception as e:
                logger.error(e)
                return JsonResponse({
                    'status': 'fail',
                    'message': 'The product does not exist.'
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'fail',
            'message': 'Please login first'
        })

def delete_review(request, review_id):
    user = request.user
    if user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            logger.info('received request to delete review')
            try:
                review = get_object_or_404(Review, id=review_id)
                logger.info('To delete: {}', review.id)
                if review.author == user:
                    try: 
                        review.delete()
                        return JsonResponse({
                            'status': 'success',
                            'message': 'This review is deleted successfully.',
                            'id': review_id
                        })
                    except Exception as e:
                        logger.error(e)
                        return JsonResponse({
                            'status': 'fail',
                            'message': 'Cannot delete this review.'
                        })
                else:
                    return JsonResponse({
                        'status': 'fail',
                        'message': 'You have not authority to delete it.'
                    })
            except Exception as e:
                logger.error(e)
                return JsonResponse({
                    'status': 'fail',
                    'message': 'This review does not exist.',
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'fail',
            'message': 'Please login first'
        })
    
