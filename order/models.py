from django.db import models
from django.db.models.fields.related import ForeignKey
from accounts.models import User
from vendor.models import Product, Vendor
import simplejson as json
import logging

logger = logging.getLogger(__name__)

# Create your models here.
request_object = ''
class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True)
    method = models.CharField(max_length=20)
    customer = ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_no
    
class Order(models.Model):

    class Status(models.TextChoices):
        NEW = ('New', 'New')
        ACCEPTED = ('Accepted', 'Accepted')
        COMPLETED = ('Completed', 'Completed')
        CANCELED = ('Canceled', 'Canceled')

    order_no = models.CharField(max_length=50, unique=True)
    customer = ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    first_name_bill = models.CharField(max_length=20, blank=True, null=True)
    last_name_bill = models.CharField(max_length=20, blank=True, null=True)
    phone_bill = models.CharField(max_length=20, blank=True, null=True)
    email_bill = models.EmailField(max_length=50, blank=True, null=True)
    address_bill = models.CharField(max_length=50, blank=True, null=True)
    city_bill = models.CharField(max_length=20, blank=True, null=True)
    state_bill = models.CharField(max_length=20, blank=True, null=True)
    country_bill = models.CharField(max_length=20, blank=True, null=True)
    zip_code_bill = models.CharField(max_length=20, blank=True, null=True)

    sub_amount = models.FloatField()
    tax_amount = models.FloatField()
    tax_data = models.JSONField(blank=True, null=True, help_text="Data format: 'tax_type': {{'percentage': 'tax_amount'}}")
    total_amount = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default='New')
    payment = ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_no
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_to_vendors(self):
        return ','.join([str(i) for i in self.vendors.all()])
    
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user) # type: ignore
        subtotal = 0
        tax = 0
        total = 0
        tax_dict = {}
        try:
            total_dict =  json.loads(self.total_data) if self.total_data else {}
            data = total_dict[str(vendor.pk)]
            for key, val in data.items():
                subtotal += float(key)
                tax_dict.update(val)
                for type, value in val.items():
                    for i, j in value.items():
                        tax += j
        except Exception as e:
            logger.error(e)
            total = 0
        total = subtotal + tax

        return {
            'subtotal': subtotal,
            'tax': tax,
            'tax_dict': tax_dict,
            'total': total,
        }

    
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
        return self.product.name
