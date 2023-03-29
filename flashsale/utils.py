from datetime import datetime
from django.core.exceptions import PermissionDenied

def generate_order_no(sale_order):
    return f"flashsale{datetime.now().strftime('%Y%m%d%H%M%S')}{sale_order.id}"

def check_role_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def get_role_url(request):
    if request.user.role == 1:
        return '/flash_sales/v/'
    if request.user.role == 2:
        return '/flash_sales/c/'