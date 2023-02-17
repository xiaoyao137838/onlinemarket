from django.db import models
from django.db.models.fields.related import OneToOneField
from accounts.models import User, UserProfile

# Create your models here.
class Vendor(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    profile = OneToOneField(UserProfile, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    slug_name = models.SlugField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    verified_file = models.ImageField(upload_to='vendor/verified_files')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name