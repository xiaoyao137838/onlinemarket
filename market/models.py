from django.db import models
from vendor.models import Product
from accounts.models import User
from django.db.models.fields.related import ForeignKey

# Create your models here.
class CartItem(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    customer = ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product
    
class Tax(models.Model):
    tax_type = models.CharField(max_length=20)
    percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax percentage (%)')

    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type