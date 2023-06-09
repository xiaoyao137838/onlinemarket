from django.urls import path
from accounts import views as accountViews
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('product_detail/<product_slug>/', views.product_detail, name='product_detail'),
    path('add_cart/<product_id>', views.add_cart, name='add_cart'),
    path('deduce_cart/<product_id>', views.deduce_cart, name='deduce_cart'),
    path('remove_cart/<cart_id>', views.remove_cart, name='remove_cart'),

    path('add_review', views.add_review, name='add_review'),
    path('delete_reivew/<review_id>', views.delete_review, name='delete_review'),
]