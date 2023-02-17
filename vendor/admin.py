from django.contrib import admin

from vendor.models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'vendor_name', 'slug_name', 'is_verified', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_verified',)

admin.site.register(Vendor, VendorAdmin)