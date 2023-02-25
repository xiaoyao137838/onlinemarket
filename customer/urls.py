from django.urls import path
from accounts import views as accountViews
from . import views

urlpatterns = [
    path('', accountViews.customer_dashboard, name='customer'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    path('customer_orders/<order_no>', views.customer_order, name='customer_order'),
]