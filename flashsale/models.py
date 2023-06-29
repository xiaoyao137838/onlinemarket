from django.db import models
from accounts.models import User
from .utils import generate_order_no
from vendor.models import Vendor, Product
from order.models import Payment

# Create your models here.
class FlashSale(models.Model):
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    old_price = models.FloatField(blank=True, null=True)
    new_price = models.FloatField()
    from_time = models.DateTimeField(blank=True, null=True)
    to_time = models.DateTimeField()
    total_qty = models.IntegerField()
    locked_qty = models.IntegerField(default=0)
    available_qty = models.IntegerField(default=0)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vendor', 'product')


class FlashOrder(models.Model):

    class Status(models.IntegerChoices):
        NO_STOCK = -1, ('No stock') 
        CREATED = 0, ('Created') 
        PAIED = 1, ('Paied')
        INVALID = 2, ('Invalid')

    order_no = models.CharField(max_length=50, unique=True)
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.SmallIntegerField(choices=Status.choices, default=0)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    sub_amount = models.FloatField()
    tax_amount = models.FloatField()
    total_amount = models.FloatField()
    tax_data = models.JSONField(blank=True, null=True, help_text="Data format: 'tax_type': {{'percentage': 'tax_amount'}}")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
