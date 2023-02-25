from vendor.models import Vendor
from .models import UserProfile

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