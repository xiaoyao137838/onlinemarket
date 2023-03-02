from vendor.models import Vendor
from .models import UserProfile
from onlinemarket.settings import PAYPAL_CLIENT_ID, GOOGLE_API_KEY

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = None
    return dict(profile=profile)

def get_google_api_key(request):
    return {'GOOGLE_API_KEY': GOOGLE_API_KEY}

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': PAYPAL_CLIENT_ID}