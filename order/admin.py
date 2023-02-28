from django.contrib import admin
from .models import Order, OrderedItem, Payment

# Register your models here.
class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    readonly_fields = ('product', 'order', 'payment', 'customer', 'quantity', 'price', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderedItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)
admin.site.register(Payment)