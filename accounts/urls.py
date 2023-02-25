from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.register_user, name='registerUser'),
    path('registerVendor/', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_validator/<uid>/<token>', views.password_reset_validator, name='password_reset_validator'),
    path('password_reset/', views.password_reset, name='password_reset'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('customer_dashboard', views.customer_dashboard, name='customer_dashboard'),
    path('vendor_dashboard', views.vendor_dashboard, name='vendor_dashboard'),
    
]