from django.urls import path
from accounts import views as accountViews
from . import views

urlpatterns = [
    path('', accountViews.vendor_dashboard, name='vendor'),
    path('vendor_profile/', views.vendor_profile, name='vendor_profile'),
    path('vendor_orders/', views.vendor_orders, name='vendor_orders'),
    path('vendor_orders/<order_no>', views.vendor_order, name='vendor_order'),

    path('products/', views.products, name='products'),
    path('products/add', views.add_product, name='add_product'),
    path('products/<id>', views.product, name='product'), 
    path('products/delete/<id>', views.delete_product, name='delete_product'),

    path('opening_hours', views.opening_hours, name='opening_hours'),
    path('opening_hours/add', views.add_opening_hour, name='add_opening_hour'),
    path('opening_hours/delete/<id>', views.delete_opening_hour, name='delete_opening_hour'),

]