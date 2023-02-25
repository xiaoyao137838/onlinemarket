from django.contrib import admin

from vendor.models import Vendor, Product, OpeningHour

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'vendor_name', 'slug_name', 'is_verified', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_verified',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'vendor', 'image', 'is_available')

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_time', 'to_time')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)