from vendor.models import Vendor
from .models import UserProfile
from onlinemarket.settings import PAYPAL_CLIENT_ID, GOOGLE_API_KEY, MAPBOX_TOKEN
import logging

logger = logging.getLogger(__name__)

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Exception as e:
        logger.error(e)
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except Exception as e:
        logger.error(e)
        profile = None
        
    return dict(profile=profile)

def get_google_api_key(request):
    return {'GOOGLE_API_KEY': GOOGLE_API_KEY}

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': PAYPAL_CLIENT_ID}

def get_mapbox_token(request):
    return {'MAPBOX_TOKEN': MAPBOX_TOKEN}