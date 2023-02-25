from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import User
from vendor.models import Product

# Create your models here.
class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True)
    method = models.CharField(max_length=20)
    Customer = ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.method
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    order_no = models.CharField(max_length=50, unique=True)
    customer = ForeignKey(User, on_delete=models.CASCADE)
    sub_amount = models.FloatField()
    tax_amount = models.FloatField()
    tax_data = models.JSONField(blank=True, null=True, help_text="Data format: {'percentage': 'tax_amount'}")
    total_amount = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    payment = ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_no
    
class OrderedItem(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    amount = models.FloatField()
    customer = ForeignKey(User, on_delete=models.CASCADE)
    order = ForeignKey(Order, on_delete=models.CASCADE)
    payment = ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product
