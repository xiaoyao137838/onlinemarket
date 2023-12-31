"""onlinemarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 
from market import views as marketViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('customer/', include('customer.urls')),
    path('vendor/', include('vendor.urls')),
    path('market/', include('market.urls')),
    path('', include('flashsale.urls')),

    #cart
    path('cart/', marketViews.cart, name='cart'),

    path('checkout/', marketViews.checkout, name='checkout'),

    path('search/', marketViews.search, name='search'),

    path('order/', include('order.urls')),

    path('postsharing/', include('postsharing.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
