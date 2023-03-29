from django.urls import path
from . import views

urlpatterns = [
    path('<vendor_slug>/flash_sales', views.flashsales, name='flashsales'),

    path('flash_sales/<product_id>/add', views.add_flashsale, name='add_flashsale'),
    path('flash_sales/delete/<id>', views.delete_flashsale, name='delete_flashsale'),
    path('flash_sales/<id>', views.flashsale, name='flashsale'),
    path('flash_sales/c/<id>', views.flashsale_customer, name='flashsale_customer'),
    path('flash_sales/v/<id>', views.flashsale_vendor, name='flashsale_vendor'),

    path('flash_select/', views.select_flash_sale, name='flash_select'),
    path('flash_checkout/<id>', views.checkout, name='flash_checkout'),
    path('flash_order/<id>', views.make_order, name='flash_make_order'),
    path('flash_payment/', views.make_payment, name='flash_make_payment'),
    path('flash_pay_done/', views.pay_done, name='flash_pay_done')
]