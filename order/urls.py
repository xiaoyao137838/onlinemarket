from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_order, name='place_order'),
    path('make_payment/', views.make_payment, name='make_payment'),
    
    path('payment_complete/', views.payment_complete, name='payment_complete'),
]