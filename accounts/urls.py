from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.register_user, name='registerUser'),
    path('registerVendor/', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('customer_dashboard', views.customer_dashboard, name='customer_dashboard'),
    path('vendor_dashboard', views.vendor_dashboard, name='vendor_dashboard'),
    
]