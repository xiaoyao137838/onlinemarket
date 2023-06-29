from .models import CartItem, Tax
from customer.views import get_customer
import logging

logger = logging.getLogger(__name__)

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.filter(customer=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except Exception as e:
            logger.error(e)
            cart_count = 0
            
    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}

    if request.user.is_authenticated:
        try:
            customer = get_customer(request)
            cart_items = CartItem.objects.filter(customer=customer)
            for cart_item in cart_items:
                subtotal += cart_item.quantity * cart_item.product.price
        except Exception as e: 
            logger.error(e)
            subtotal = 0    

        try:
            tax_obj = Tax.objects.get(tax_type='Tax')
            tax = subtotal * float(tax_obj.percentage) / 100
            tax = round(tax, 2)
            tax_dict = {tax_obj.tax_type: {str(tax_obj.percentage): tax}}
            grand_total = subtotal + tax
        except Exception as e: 
            logger.error(e)
            subtotal = 0

    return dict(subtotal=round(subtotal, 2), tax=tax, tax_dict=tax_dict, grand_total=round(grand_total, 2))