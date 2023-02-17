from django.core.exceptions import PermissionDenied

def check_role_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def get_role_url(request):
    user = request.user
    if user.role == 1:
        return 'vendor_dashboard'
        
    if user.role == 2:
        return 'customer_dashboard'
    if user.is_admin:
        return '/admin'