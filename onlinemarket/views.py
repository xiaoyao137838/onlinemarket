from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def home(request):
    current_location_info = get_or_set_current_location(request)
    if current_location_info:
        lat, lng = current_location_info
        longitude = lng
        latitude = lat
        pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        vendors = Vendor.objects.filter(is_verified=True, user__is_active=True, profile__location__distance_lte=(pnt, D(km=100))).annotate(distance=Distance("profile__location", pnt)).order_by("distance")[:6]

        for vendor in vendors:
            vendor.kms = round(vendor.distance.km, 1)
    else:
        vendors = Vendor.objects.filter(is_verified=True, user__is_active=True)[:6]

    context = {
        'vendors': vendors,
    }
    return render(request, 'home.html', context)

def get_or_set_current_location(request):
    if 'lat' in request.session and 'lng' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lat, lng
    elif 'lat' in request.GET and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lat, lng
    else:
        return None