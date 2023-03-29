from django.contrib import admin
from .models import FlashOrder, FlashSale

# Register your models here.
# class FlashOrderInline(admin.TabularInline):
#     model = FlashOrder
#     readonly_fields = ('order_no', 'product', 'flash_sale', 'customer', 'total_amount')
#     extra = 0

# class FlashOrderAdmin(admin.ModelAdmin):
#     inlines = [FlashOrderInline]

admin.site.register(FlashSale)
admin.site.register(FlashOrder)
# admin.site.register(FlashOrder, FlashOrderAdmin)
