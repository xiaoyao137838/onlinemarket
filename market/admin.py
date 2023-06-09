from django.contrib import admin
from .models import CartItem, Review, Tax
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'modified_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'percentage')

admin.site.register(CartItem, CartAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Review)